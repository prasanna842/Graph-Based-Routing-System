# Makefile
SHELL := /bin/bash

# Compiler and flags - Modern C++20
CXX = g++
CXXFLAGS = -g -Wall -Wextra -std=c++20 -O3

# Executable name
EXEC1 = phase1 
EXEC2 = phase2
EXEC3 = phase3

DIR1 = Phase-1/
DIR2 = Phase-2/
DIR3 = Phase-3/
# Source files
HEADERS1 = $(DIR1)graph.hpp
HEADERS2 = $(DIR2)graph.hpp
HEADERS3 = $(DIR3)graph.hpp

SOURCES1 = $(DIR1)read_graph.cpp $(DIR1)dynamic_updates.cpp $(DIR1)shortest_path.cpp $(DIR1)knn.cpp $(DIR1)main.cpp
SOURCES2 = $(DIR2)read_graph.cpp $(DIR2)k_shortest_paths.cpp $(DIR2)k_shortest_paths_heuristic.cpp $(DIR2)approx_shortest_path.cpp $(DIR2)main.cpp
SOURCES3 = $(DIR3)read_graph.cpp $(DIR3)main.cpp

# Object files
OBJECTS1 = $(SOURCES1:.cpp=.o)
OBJECTS2 = $(SOURCES2:.cpp=.o)
OBJECTS3 = $(SOURCES3:.cpp=.o)

# Test configuration

# Default target
all: phase1 phase2 phase3 gentest1 gentest2 gentest3
# Build target
gentest1:
	python3 tester_phase1.py

gentest2:
	python3 tester_phase2.py

gentest3:
	python3 tester_phase3.py

# Link executable
$(EXEC1): $(OBJECTS1) $(HEADERS1)
	$(CXX) $(CXXFLAGS) -o $(EXEC1) $(OBJECTS1)

$(EXEC2): $(OBJECTS2) $(HEADERS2)
	$(CXX) $(CXXFLAGS) -o $(EXEC2) $(OBJECTS2)

$(EXEC3): $(OBJECTS3) $(HEADERS3)
	$(CXX) $(CXXFLAGS) -o $(EXEC3) $(OBJECTS3)

# Compile object files
%.o: %.cpp *.hpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean build artifacts
clean:
	rm -f $(OBJECTS1) $(EXEC1) $(OBJECTS2) $(EXEC2) $(OBJECTS3) $(EXEC3) output.txt
	find . -type f -name '*~'  -delete

.PHONY: all build runtests clean