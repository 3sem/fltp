#!/bin/bash

# Input C file
C_FILE="input.c"
# Output LLVM IR file
LLVM_IR_FILE="output.ll"
# Optimized LLVM IR file
OPTIMIZED_LLVM_IR_FILE="optimized_output.ll"
# Output binary file
OUTPUT_BINARY="output_binary"

# Step 1: Compile C code to LLVM IR
echo "Compiling C code to LLVM IR..."
clang -S -emit-llvm -o $LLVM_IR_FILE $C_FILE

# Check if LLVM IR generation succeeded
if [ ! -f $LLVM_IR_FILE ]; then
    echo "Error: Failed to generate LLVM IR."
    exit 1
fi

# Step 2: Search for and apply optimal optimizations
echo "Applying optimizations to LLVM IR..."
opt -S -O3 -o $OPTIMIZED_LLVM_IR_FILE $LLVM_IR_FILE

# Check if optimization succeeded
if [ ! -f $OPTIMIZED_LLVM_IR_FILE ]; then
    echo "Error: Failed to optimize LLVM IR."
    exit 1
fi

# Step 3: Compile optimized LLVM IR to binary
echo "Compiling optimized LLVM IR to binary..."
llc -filetype=obj -o output.o $OPTIMIZED_LLVM_IR_FILE
clang -o $OUTPUT_BINARY output.o

# Check if binary generation succeeded
if [ ! -f $OUTPUT_BINARY ]; then
    echo "Error: Failed to generate binary."
    exit 1
fi

echo "Pipeline completed successfully. Binary generated: $OUTPUT_BINARY"
