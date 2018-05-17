#include "NoiseFilter.h"

NoiseFilter::NoiseFilter(double alpha, unsigned samplesize, double leakytau)
  : _alpha(alpha), _samplesize(samplesize), _leakytau(leakytau)
{
  _mem_re_size = 2 * _samplesize;
  _mem_fwtr_size = 1 + _mem_re_size / 2;
  _mem_rwtr_size = _mem_re_size;
  _compute_response();
}

NoiseFilter::~NoiseFilter()
{
  delete[] _response;
}

void NoiseFilter::filter(double* in, double* out)
{
  double tmp_r, tmp_i;
  fftw_complex* transfin = new fftw_complex[_mem_fwtr_size];
  // FWD DFT plan
  fftw_plan forwardtransplan = fftw_plan_dft_r2c_1d(_mem_re_size, in, transfin, FFTW_MEASURE);
  // RW DFT plan
  fftw_plan backwardtransplan = fftw_plan_dft_c2r_1d(_mem_re_size, transfin, out, FFTW_MEASURE);
  // Perform DFT on input.
  fftw_execute(forwardtransplan);
  // Apply response matrix in transformed space.
  for(unsigned j = 0; j < _samplesize; ++j)
  {
    tmp_r = transfin[j][0];
    tmp_i = transfin[j][1];
    transfin[j][0] = tmp_r * _response[j][0] - tmp_i * _response[j][1];
    transfin[j][1] = tmp_r * _response[j][1] + tmp_i * _response[j][0];
  }
  // Apply low-pass filter.
  _leak(transfin, _samplesize);
  // Perform inverse DFT on the result.
  fftw_execute(backwardtransplan);
  // Rescale output, to correct for unnormalized DFT
  for(unsigned k = 0; k < _mem_re_size; ++k)
    out[k] /= ( (double)_samplesize );
  // Free memory of the intermediate result in transformed space.
  delete[] transfin;
  // Delete DFT plans.
  fftw_destroy_plan(forwardtransplan);
  fftw_destroy_plan(backwardtransplan);
}

void NoiseFilter::_compute_response()
{
  // Kasdin, N. (1995). Discrete Simulation of Colored Noise and Stochastic Processes and 1/f^alpha Power Law Noise Generation. Proceedings of the IEEE. 83. 802 - 827. 10.1109/5.381848. 
  double* realspaceResponse;
  realspaceResponse = new double[_mem_re_size];
  _response = new fftw_complex[_mem_fwtr_size];
  fftw_plan forwardtransplan = fftw_plan_dft_r2c_1d(_mem_re_size, realspaceResponse, _response, FFTW_MEASURE);
  // Initialize response matrix in direct space. 
  realspaceResponse[0] = 1.;
  for(unsigned i = 1; i < _samplesize; ++i)
    realspaceResponse[i] = (0.5 * _alpha + (double)i - 1.) * realspaceResponse[i-1] / ((double)i);
  for(unsigned j = _samplesize; j < 2 * _samplesize; ++j)
    realspaceResponse[j] = 0.;
  // Calculate the real dft of the response matrix.
  fftw_execute(forwardtransplan);
  // Only keep the transformed space response matrix stored.
  fftw_destroy_plan(forwardtransplan);
  delete[] realspaceResponse;
}

void NoiseFilter::_leak(fftw_complex* signal, unsigned size)
{
  if(_leakytau <= 0.)
    return;
  else
  {
    // Leak:
    // Amounts to dividing by (leakytau + sqrt(-1) * omega)
    // As can be seen transforming the equation dy/dt = -leakytau * y + x
    // where y is the output and x is the input.

    double tmp_r, tmp_i;
    double l1, l2, lden;

    for(unsigned i = 0; i < size; ++i)
    {
      lden =  _leakytau * _leakytau + (double)(i * i);
      l1 = _leakytau / lden;
      l2 = (double)i / lden;
      tmp_r = signal[i][0];
      tmp_i = signal[i][1];
      signal[i][0] = l1 * tmp_r + l2 * tmp_i;
      signal[i][1] = l1 * tmp_i - l2 * tmp_r;
    }
  }
}
