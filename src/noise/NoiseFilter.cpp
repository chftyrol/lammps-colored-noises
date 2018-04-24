#include "NoiseFilter.h"

NoiseFilter::NoiseFilter(double alpha, unsigned samplesize)
  : _alpha(alpha), _samplesize(samplesize)
{
  _mem_re_size = _samplesize;
  _mem_fwtr_size = 1 + _samplesize / 2;
  _mem_rwtr_size = 2 + _samplesize;
  compute_response();
}

NoiseFilter::~NoiseFilter()
{
  delete[] _response;
}

void NoiseFilter::filter(double* in, double* out)
{
  double tmp_r, tmp_i;
  // Perform DFT on input.
  fftw_complex* transfin = new fftw_complex[_mem_fwtr_size];
  fwDft(in, transfin, FFTW_ESTIMATE);
  // Apply response matrix in transformed space.
  for(unsigned j = 0; j < _mem_fwtr_size; ++j)
  {
    tmp_r = transfin[j][0];
    tmp_i = transfin[j][1];
    transfin[j][0] = tmp_r * _response[j][0] - tmp_i * _response[j][1];
    transfin[j][1] = tmp_r * _response[j][1] + tmp_i * _response[j][0];
  }
  // Perform inverse DFT on the result.
  rwDft(transfin, out, FFTW_ESTIMATE);
  // Rescale output, to correct for unnormalized DFT
  for(unsigned k = 0; k < _mem_re_size; ++k)
    out[k] /= ((double)_samplesize) ;
  // Free memory of the intermediate result in transformed space.
  delete[] transfin;
}

void NoiseFilter::compute_response()
{
  // Kasdin, N. (1995). Discrete Simulation of Colored Noise and Stochastic Processes and 1/f^alpha Power Law Noise Generation. Proceedings of the IEEE. 83. 802 - 827. 10.1109/5.381848. 
  double* realspaceResponse;
  realspaceResponse = new double[_mem_re_size];
  _response = new fftw_complex[_mem_fwtr_size];
  // Initialize response matrix in direct space. 
  realspaceResponse[0] = 1.;
  for(unsigned i = 1; i < _samplesize; ++i)
  {
    realspaceResponse[i] = (0.5 * _alpha + (double)i - 1.) * realspaceResponse[i-1] / ((double)i);
  }
  // Calculate the real dft of the response matrix.
  fwDft(realspaceResponse, _response, FFTW_ESTIMATE);
  // Only keep the transformed space response matrix stored.
  delete[] realspaceResponse;
}

void NoiseFilter::fwDft(double* in, fftw_complex* out, unsigned fft_flags)
{
  fftw_plan forwardtransplan = fftw_plan_dft_r2c_1d(_samplesize, in, out, fft_flags);
  fftw_execute(forwardtransplan);
  fftw_destroy_plan(forwardtransplan);
}

void NoiseFilter::rwDft(fftw_complex* in, double* out, unsigned fft_flags)
{
  fftw_plan backwardtransplan = fftw_plan_dft_c2r_1d(_samplesize, in, out, fft_flags);
  fftw_execute(backwardtransplan);
  fftw_destroy_plan(backwardtransplan);
}
