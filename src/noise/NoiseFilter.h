#include <stdio.h>
#include <fftw3.h>

#ifndef __NOISEFILTER_H__
#define __NOISEFILTER_H__

class NoiseFilter
{
  public:
    NoiseFilter(double alpha, unsigned samplesize=1024, int fft_flags=FFTW_ESTIMATE);
    ~NoiseFilter();

    void filter(fftw_complex* in, fftw_complex* out);
  private:
    double _alpha;
    unsigned _samplesize;
    int _fft_flags;
    fftw_complex* _response; // Eigenvalues of the response matrix.
    void compute_response(); // Calculate response matrix (directly in diagonal form).
    void fwDft(fftw_complex* in, fftw_complex* out); // Forward DFT.
    void rwDft(fftw_complex* in, fftw_complex* out); // Backward DFT.
};

#endif // __NOISEFILTER_H__
