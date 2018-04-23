OBJECTS = main.o WhiteNoise.o
CXXFLAGS = -Wall -pipe -std=c++11
TARGET = WhiteNoise.x

.PHONY = clean

$(TARGET): $(OBJECTS)
	$(LINK.cc) -o $@ $^
%.o: %.cpp
	$(COMPILE.cc) $<
clean:
	$(RM) $(OBJECTS)
cleanall:
	$(RM) $(OBJECTS) $(TARGET)
