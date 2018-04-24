#include "NoiseFilter.h"

NoiseFilter::NoiseFilter(double alpha, unsigned samplesize, int fft_flags)
  : _alpha(alpha), _samplesize(samplesize), _fft_flags(fft_flags)
{
  compute_response();
}

NoiseFilter::~NoiseFilter()
{
  delete[] _response;
}

void NoiseFilter::filter(fftw_complex* in, fftw_complex* out)
{
  double tmp_r, tmp_i;
  // Perform DFT on input.
  fftw_complex* transfin = new fftw_complex[_samplesize];
  fwDft(in, transfin);
  // Apply response matrix in transformed space.
  for(unsigned j = 0; j < _samplesize; ++j)
  {
    tmp_r = transfin[j][0];
    tmp_i = transfin[j][1];
    transfin[j][0] = tmp_r * _response[j][0] - tmp_i * _response[j][1];
    transfin[j][1] = tmp_r * _response[j][1] + tmp_i * _response[j][0];
  }
  // Perform inverse DFT on the result.
  rwDft(transfin, out);
  // Free memory of the intermediate result in transformed space.
  delete[] transfin;
}

void NoiseFilter::compute_response()
{
  // Kasdin, N. (1995). Discrete Simulation of Colored Noise and Stochastic Processes and 1/f^alpha Power Law Noise Generation. Proceedings of the IEEE. 83. 802 - 827. 10.1109/5.381848. 
  _response = new fftw_complex[_samplesize];
  _response[0][0] = 1.;
  _response[0][1] = 0.;
  for(unsigned i = 1; i < _samplesize; ++i)
  {
    _response[i][0] = (0.5 * _alpha + (double)i - 1.) * _response[i-1][0] / ((double)i);
    _response[i][1] = 0.;
  }

  fwDft(_response, _response);
}

void NoiseFilter::fwDft(fftw_complex* in, fftw_complex* out)
{
  fftw_plan forwardtransplan = fftw_plan_dft_1d(_samplesize, in, out, FFTW_FORWARD, _fft_flags);
  fftw_execute(forwardtransplan);
  fftw_destroy_plan(forwardtransplan);
}

void NoiseFilter::rwDft(fftw_complex* in, fftw_complex* out)
{
  fftw_plan backwardtransplan = fftw_plan_dft_1d(_samplesize, in, out, FFTW_BACKWARD, _fft_flags);
  fftw_execute(backwardtransplan);
  fftw_destroy_plan(backwardtransplan);
}
