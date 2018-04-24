#include <fftw3.h>

#ifndef __NOISEFILTER_H__
#define __NOISEFILTER_H__

class NoiseFilter
{
  public:
    NoiseFilter(double alpha, unsigned samplesize=1024);
    ~NoiseFilter();

    void filter(double* in, double* out); 
  private:
    double _alpha;
    unsigned _samplesize;
    unsigned _mem_re_size;
    unsigned _mem_fwtr_size;
    unsigned _mem_rwtr_size;
    fftw_complex* _response; // Eigenvalues of the response matrix.
    void compute_response(); // Calculate response matrix (directly in diagonal form).
    void fwDft(double* in, fftw_complex* out, unsigned fft_flags); // Forward DFT.
    void rwDft(fftw_complex* in, double* out, unsigned fft_flags); // Backward DFT.
};

#endif // __NOISEFILTER_H__
