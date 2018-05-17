#include <fftw3.h>

#ifndef __NOISEFILTER_H__
#define __NOISEFILTER_H__

class NoiseFilter
{
  public:
    NoiseFilter(double alpha, unsigned samplesize=1024, double leakytau=0.);
    ~NoiseFilter();

    void filter(double* in, double* out); 
    /* USAGE:
     * in: double* of size 2 * samplesize.
     *          the first half (from 0 to samplesize -1) must contain the signal to be filtered.
     *          the second half (from samplesize to 2 * samplesize - 1) must contain 0.0.
     * out: double* of size 2 * samplesize. Will contain the output signal, padded with zeroes at the end, just like in.
     *
     * Both in and out must be allocated prior to sending the to filter.
     */
  private:
    double _alpha;
    unsigned _samplesize;
    double _leakytau;
    unsigned _mem_re_size;
    unsigned _mem_fwtr_size;
    unsigned _mem_rwtr_size;
    fftw_complex* _response; // Eigenvalues of the response matrix.
    void _compute_response(); // Calculate response matrix (directly in diagonal form).
    void _leak(fftw_complex*, unsigned);
};

#endif // __NOISEFILTER_H__
