# Signal Tests

This test suite covers the signal functionality in the Android application.

## Test Cases

### SGL_TC01 - Add/Remove Signal from Favourites
- **File**: `test_SGL_TC01_positive_add_remove_signal_from_favourites.py`
- **Purpose**: Verify members can add and remove signals from their favourites list
- **Steps**:
  1. Navigate to Signal page
  2. Add signal to favourites from Signal List
  3. Verify signal appears in Favourites tab
  4. Remove signal from favourites
  5. Verify signal no longer appears in Favourites tab

### SGL_TC02 - Copy Signal to Order
- **File**: `test_SGL_TC02_positive_copy_signal_to_order.py`
- **Purpose**: Verify members can copy signals to trade orders and submit them
- **Steps**:
  1. Navigate to Signal page
  2. Select a signal to copy
  3. Copy signal to order
  4. Verify trade order panel is populated with signal data
  5. Submit the copied order
  6. Verify trade confirmation
  7. Confirm order placement

### SGL_TC03 - Favourite Signal Copy to Order
- **File**: `test_SGL_TC03_positive_favourite_signal_copy_to_order.py`
- **Purpose**: Verify members can copy favourite signals to trade orders
- **Steps**:
  1. Navigate to Signal page
  2. Add signal to favourites
  3. Verify signal in Favourites tab
  4. Copy favourite signal to order
  5. Verify trade order panel populated with signal data
  6. Submit the copied order
  7. Verify trade confirmation and confirm order

## Prerequisites

- User must be logged into the application
- Signal functionality must be available
- Trading functionality must be enabled

## Test Configuration

The tests use the standard Android test configuration with automatic login setup via `conftest.py`.