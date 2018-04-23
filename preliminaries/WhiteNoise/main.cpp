#include <iostream>
#include "WhiteNoise.h"

int main(int argc, char** argv)
{
  // If a seed is not specified, the class uses the seconds since the Unix epoch.
  const unsigned seed = 77;
  WhiteNoise wn(0., 1., seed);

  const unsigned count = 1000;

  // i acts as a upper integration limit
  for(unsigned i = 1; i <= count; ++i) 
  {
    std::cout << i << "\t" << wn() << std::endl;
  }
  return 0;
}
