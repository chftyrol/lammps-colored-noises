OBJECTS = tester.o NoiseFilter.o WhiteNoise.o ColoredNoise.o
CXXFLAGS = -Wall -pipe -std=c++11
LDFLAGS = -lfftw3 -lm
TARGET = tester.x

.PHONY = clean

$(TARGET): $(OBJECTS)
	$(LINK.cc) -o $@ $^
%.o: %.cpp
	$(COMPILE.cc) $<
clean:
	$(RM) $(OBJECTS)
cleanall:
	$(RM) $(OBJECTS) $(TARGET)
