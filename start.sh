#!/bin/bash
echo "========== BOOT LOGS =========="
echo "Current directory: $(pwd)"
echo "Listing repo:"
ls -R .
echo "================================"

echo "Setting PYTHONPATH so Streamlit can import the local package..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "PYTHONPATH is now: ${PYTHONPATH}"

echo "Launching Streamlit..."
streamlit run app/main.py --server.address 0.0.0.0 --server.port $PORT
