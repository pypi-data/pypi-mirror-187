/* PyVkFFT
   (c) 2021- : ESRF-European Synchrotron Radiation Facility
       authors:
         Vincent Favre-Nicolin, favre@esrf.fr
*/

// We use the CUDA backend
#define VKFFT_BACKEND 1

#include <iostream>
#include <fstream>
#include <memory>
using namespace std;
#include "vkFFT.h"
typedef float2 Complex;

#ifdef _WIN32
#define LIBRARY_API extern "C" __declspec(dllexport)
#else
#define LIBRARY_API extern "C"
#endif


LIBRARY_API VkFFTConfiguration* make_config(const size_t, const size_t, const size_t, const size_t, void*, void*, void*,
                                const int, const size_t, const int, const int, const int, const int,
                                const int, const int, const size_t, const int, const int, const int);

LIBRARY_API VkFFTApplication* init_app(const VkFFTConfiguration*, int*);

LIBRARY_API int fft(VkFFTApplication* app, void*, void*);

LIBRARY_API int ifft(VkFFTApplication* app, void*, void*);

LIBRARY_API void free_app(VkFFTApplication* app);

LIBRARY_API void free_config(VkFFTConfiguration *config);

LIBRARY_API uint32_t vkfft_version();

LIBRARY_API int cuda_runtime_version();

LIBRARY_API int cuda_driver_version();

LIBRARY_API int cuda_compile_version();


class PyVkFFT
{
  public:
    PyVkFFT(const int nx, const int ny, const int nz, const int fftdim, void* hstream,
            const int norm, const int precision, const int r2c)
    {

    };
  private:
    VkFFTConfiguration mConf;
    VkFFTApplication mApp;
    VkFFTApplication mLaunchParams;
};


/** Create the VkFFTConfiguration from the array parameters
*
* \param nx, ny, nz: dimensions of the array. The fast axis is x. In the corresponding numpy array,
* this corresponds to a shape of (nz, ny, nx)
* \param fftdim: the dimension of the transform. If nz>1 and fftdim=2, the transform is only made
* on the x and y axes
* \param buffer, buffer_out: pointer to the GPU data source and destination arrays. These
*  can be fake and the actual buffers supplied in fft() and ifft. However buffer should be non-zero,
*  and buffer_out should be non-zero only for an out-of-place transform.
* \param hstream: the stream handle (CUstream)
* \param norm: 0, the L2 norm is multiplied by the size on each transform, 1, the inverse transform
*   divides the L2 norm by the size.
* \param precision: number of bits per float, 16=half, 32=single, 64=double precision
* \return: the pointer to the newly created VkFFTConfiguration, or 0 if an error occurred.
*/
VkFFTConfiguration* make_config(const size_t nx, const size_t ny, const size_t nz, const size_t fftdim,
                                void *buffer, void *buffer_out, void* hstream,
                                const int norm, const size_t precision, const int r2c, const int dct,
                                const int disableReorderFourStep, const int registerBoost,
                                const int useLUT, const int keepShaderCode, const size_t n_batch,
                                const int skipx, const int skipy, const int skipz)
{
  VkFFTConfiguration *config = new VkFFTConfiguration({});
  config->FFTdim = fftdim;
  config->size[0] = nx;
  config->size[1] = ny;
  config->size[2] = nz;
  config->numberBatches = n_batch;

  config->omitDimension[0] = skipx;
  config->omitDimension[1] = skipy;
  config->omitDimension[2] = skipz;

  config->normalize = norm;
  config->performR2C = r2c;
  config->performDCT = dct;

  if(disableReorderFourStep>=0)
    config->disableReorderFourStep = disableReorderFourStep;

  if(registerBoost>=0)
    config->registerBoost = registerBoost;

  if(useLUT>=0)
    config->useLUT = useLUT;

  if(keepShaderCode>=0)
    config->keepShaderCode = keepShaderCode;

  switch(precision)
  {
      case 2 : config->halfPrecision = 1;
      case 8 : config->doublePrecision = 1;
  };

  CUdevice *dev = new CUdevice;
  if(hstream != 0)
  {
    // Get context then device from current context
    CUcontext ctx = nullptr;
    CUresult res = cuStreamGetCtx ((CUstream)hstream, &ctx);
    if(res != CUDA_SUCCESS)
    {
      cout << "Could not get the current device from given stream"<<endl;
      return 0;
    }
    res = cuCtxPushCurrent (ctx);
    res = cuCtxGetDevice(dev);
    if(res != CUDA_SUCCESS)
    {
      cout << "Could not get the current device from supplied stream's context."<<endl;
      return 0;
    }
    res = cuCtxPopCurrent (&ctx);

    config->stream = new CUstream((CUstream) hstream);
    config->num_streams = 1;
  }
  else
  {
    // Get device from current context
    CUresult res = cuCtxGetDevice(dev);
    if(res != CUDA_SUCCESS)
    {
      cout << "Could not get the current device. Was a CUDA context created ?"<<endl;
      return 0;
    }
  }
  config->device = dev;

  void ** pbuf = new void*;
  *pbuf = buffer;

  uint64_t* psize = new uint64_t;
  uint64_t* psizein = psize;

  if(r2c)
  {
    *psize = (uint64_t)((nx / 2 + 1) * ny * nz * precision * (size_t)2);
    if(buffer_out != NULL)
    {
      psizein = new uint64_t;
      *psizein = (uint64_t)(nx * ny * nz * precision);
      config->inverseReturnToInputBuffer = 1;
			config->inputBufferStride[0] = nx;
			config->inputBufferStride[1] = nx * ny;
			config->inputBufferStride[2] = nx * ny * nz;
    }
  }
  else
  {
    if(dct) *psize = (uint64_t)(nx * ny * nz * precision);
    else *psize = (uint64_t)(nx * ny * nz * precision * (size_t)2);
  }

  config->bufferSize = psize;

  if(buffer_out != NULL)
  {
    // Calculations are made in buffer, so with buffer != inputBuffer we keep the original data
    void ** pbufout = new void*;
    *pbufout = buffer_out;

    config->buffer = pbufout;
    config->inputBuffer = pbuf;

    config->inputBufferSize = psizein;

    config->isInputFormatted = 1;
  }
  else
  {
    config->buffer = pbuf;
  }

  /*
  cout << "make_config: "<<config<<" "<<endl<< config->buffer<<", "<< *(config->buffer)<<", "
       << config->size[0] << " " << config->size[1] << " " << config->size[2] << " "<< config->FFTdim
       << " " << *(config->bufferSize) << endl;
  */
  return config;
}

/** Initialise the VkFFTApplication from the given configuration.
*
* \param config: the pointer to the VkFFTConfiguration
* \return: the pointer to the newly created VkFFTApplication
*/
VkFFTApplication* init_app(const VkFFTConfiguration* config, int *res)
{
  VkFFTApplication* app = new VkFFTApplication({});
  *res = initializeVkFFT(app, *config);
  /*
  cout << "init_app: "<<config<<endl<< config->buffer<<", "<< *(config->buffer)<<", "
       << config->size[0] << " " << config->size[1] << " " << config->size[2] << " "<< config->FFTdim
       << " " << *(config->bufferSize) << endl<<endl;
  cout<<res<<endl<<endl;
  */
  if(*res!=0)
  {
    delete app;
    return 0;
  }
  return app;
}

int fft(VkFFTApplication* app, void *in, void *out)
{
  // Modify the original app only to avoid allocating
  // new buffer pointers in memory
  *(app->configuration.buffer) = out;
  *(app->configuration.inputBuffer) = in;
  *(app->configuration.outputBuffer) = out;

  VkFFTLaunchParams par = {};
  par.buffer =  app->configuration.buffer;
  par.inputBuffer = app->configuration.inputBuffer;
  par.outputBuffer = app->configuration.outputBuffer;

  return VkFFTAppend(app, -1, &par);
}

int ifft(VkFFTApplication* app, void *in, void *out)
{
  // Modify the original app only to avoid allocating
  // new buffer pointers in memory
  *(app->configuration.buffer) = out;
  *(app->configuration.inputBuffer) = in;
  *(app->configuration.outputBuffer) = out;

  VkFFTLaunchParams par = {};
  par.buffer =  app->configuration.buffer;
  par.inputBuffer = app->configuration.inputBuffer;
  par.outputBuffer = app->configuration.outputBuffer;

  return VkFFTAppend(app, 1, &par);
}

/** Free memory allocated during make_config()
*
*/
void free_app(VkFFTApplication* app)
{
  if(app != NULL)
  {
    deleteVkFFT(app);
    free(app);
  }
}

/** Free memory associated to the vkFFT app
*
*/
void free_config(VkFFTConfiguration *config)
{
  free(config->device);
  // Only frees the pointer to the buffer pointer, not the buffer itself.
  free(config->buffer);
  free(config->bufferSize);

  if((config->outputBuffer != NULL) && (config->buffer != config->outputBuffer)) free(config->outputBuffer);
  if((config->inputBuffer != NULL) && (config->buffer != config->inputBuffer)
     && (config->outputBuffer != config->inputBuffer)) free(config->inputBuffer);

  if((config->inputBufferSize != NULL) && (config->inputBufferSize != config->bufferSize))
    free(config->inputBufferSize);
  if((config->outputBufferSize != NULL) && (config->outputBufferSize != config->bufferSize)
     && (config->outputBufferSize != config->inputBufferSize)) free(config->outputBufferSize);

  if(config->stream != 0) free(config->stream);
  free(config);
}

/// Get VkFFT version
uint32_t vkfft_version()
{
  return VkFFTGetVersion();
};

/// CUDA runtime version
int cuda_runtime_version()
{
  int v=0;
  const cudaError_t err = cudaRuntimeGetVersion(&v);
  if(err==cudaSuccess) return v;
  return 0;
};

/// CUDA driver version
int cuda_driver_version()
{
  int v=0;
  const CUresult err = cuDriverGetVersion(&v);
  if(err==CUDA_SUCCESS) return v;
  return 0;
};

/// CUDA version against which pyvkfft was compiled
int cuda_compile_version()
{
  return (int)CUDA_VERSION;
};
