# odin-gpio Setup Guide

A GPIO interface adapter for ODIN control system that enables triggering and GPIO control through the ODIN framework.

## Overview

The odin-gpio project provides a Trigger Adapter that integrates with ODIN control to handle GPIO operations via HTTP API. It communicates with external systems through ZMQ (ZeroMQ) for real-time event handling.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning dependencies)
- SSH access to GitHub (for cloning private repositories)

## Installation

### 1. Clone and Navigate to Project

### 2. Install Dependencies

Navigate to the server directory and install the package with its dependencies:

```bash
cd server
pip install -e .
```

This will install:
- **odin-control**: The main ODIN framework (from GitHub)
- **trigger-adapter**: This adapter package

## Configuration

The adapter is configured via [config/config.cfg](server/src/trigger_adapter/config/config.cfg).

### Key Configuration Settings

**Server Configuration:**
```ini
[server]
debug_mode = 1              # Enable debug logging
http_port = 8888            # HTTP server port
http_addr = 192.168.0.13    # HTTP server IP address
adapters = trigger_adapter  # Enabled adapters
```

**Tornado Settings:**
```ini
[tornado]
logging = debug             # Logging level
```

**Adapter Configuration:**
```ini
[adapter.trigger_adapter]
module = trigger_adapter.adapter.TriggerAdapter  # Adapter module path
```

### Before Running - Update Configuration

Update the IP addresses in [config/config.cfg](server/src/trigger_adapter/config/config.cfg) to match your network:

1. **http_addr**: Change to your server's IP address (currently `192.168.0.13`)
2. **ctrl_endpoint** in controller: Change to your control endpoint (currently `tcp://192.168.0.58:5555`)

See [controller.py](server/src/trigger_adapter/controller.py) line 19 to update the ZMQ endpoint.

## Running the ODIN Control Server

### Start the Server

```bash
cd server
odin_control --config config/config.cfg
```

The server will start and bind to the configured `http_addr` and `http_port`.

## Architecture

### Components

- **TriggerAdapter**: REST API adapter that implements HTTP GET/PUT handlers
- **TriggerController**: Manages ZMQ communication and GPIO control logic
- **ODIN Framework**: Provides the adapter and parameter tree infrastructure

### Communication Flow

1. HTTP requests arrive at TriggerAdapter
2. Adapter delegates to TriggerController
3. Controller sends/receives messages via ZMQ to external systems
4. Events are processed and responses returned

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError: No module named 'odin'`:

```bash
# Ensure you're in the server directory
cd server

# Reinstall in editable mode
pip install -e .
```

### Connection Refused

If you get connection errors when starting the server:

1. Verify IP addresses in config match your network
2. Check firewall allows traffic on the configured port
3. Ensure no other service is using the port

### ZMQ Connection Issues

If the TriggerController can't connect to the ZMQ endpoint:

1. Verify the `ctrl_endpoint` in [controller.py](server/src/trigger_adapter/controller.py) is correct
2. Ensure the external ZMQ server is running
3. Check network connectivity: `ping 192.168.0.58`
