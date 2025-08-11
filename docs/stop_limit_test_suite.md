# Stop Limit Test Suite Documentation

## Overview

The Stop Limit test suite (`tests/web_app/trade/stop_limit/`) validates the complete lifecycle of stop limit order functionality in the web trading application. This suite ensures that users can successfully place, modify, and delete stop limit orders with various configurations including Stop Loss (SL) and Take Profit (TP) parameters.

## Test Suite Structure

```
tests/web_app/trade/stop_limit/
├── __init__.py
├── conftest.py                                                    # Test fixtures
├── test_TRD_STPLMT_TC01_positive_place_order.py                  # Order placement
├── test_TRD_STPLMT_TC02_positive_modify_order_placed_without_sl_tp.py  # Modify orders without SL/TP
├── test_TRD_STPLMT_TC03_positive_modify_order_placed_with_sl_or_tp.py   # Modify orders with partial SL/TP
├── test_TRD_STPLMT_TC04_positive_modify_order_placed_with_sl_and_tp.py  # Modify orders with full SL/TP
├── test_TRD_STPLMT_TC05_positive_delete_order.py                 # Order deletion
├── test_TRD_STPLMT_TC07_positive_cancel_place_order.py           # Cancel order placement
├── test_TRD_STPLMT_TC08_positive_place_order_compare_against_api_data.py  # API validation
└── test_TRD_STPLMT_TC09_positive_modify_order_compare_against_api_data.py # API validation
```

## Test Fixtures

### `stop_limit_obj` Fixture
- **Purpose**: Creates stop limit trade objects with configurable parameters
- **Returns**: Handler function that generates `ObjTrade` instances with `OrderType.STOP_LIMIT`
- **Usage**: Provides consistent test data structure across all test cases

## Test Cases Analysis

### TC01: Place Stop Limit Order (`test_TRD_STPLMT_TC01_positive_place_order.py`)

**Purpose**: Validates successful placement of stop limit orders with various SL/TP combinations

**Test Scenarios**:
- Order without SL and TP
- Order with only SL (random values)
- Order with only TP (random values)  
- Order with both SL and TP (sample values)

**Test Flow**:
1. Get current pending orders tab amount
2. Place stop limit order with specified SL/TP configuration
3. Verify trade confirmation modal
4. Confirm order placement
5. Verify order submitted notification
6. Verify pending orders tab count increased
7. Validate order details in pending orders tab

**Validations**:
- Trade confirmation modal displays correct order details
- Success notification banner appears
- Pending orders tab count increments by 1
- Order appears in pending orders with correct details

---

### TC02: Modify Order Without SL/TP (`test_TRD_STPLMT_TC02_positive_modify_order_placed_without_sl_tp.py`)

**Purpose**: Tests modification of orders initially placed without SL/TP parameters

**Test Scenarios**:
- Add only SL to existing order
- Add only TP to existing order
- Add both SL and TP (PRICE type)
- Add both SL and TP (POINTS type)
- Add both SL and TP (random types)

**Test Flow**:
1. Place order without SL and TP
2. Verify order exists in pending orders tab
3. Modify order to add SL/TP parameters
4. Verify edit confirmation modal
5. Confirm order update
6. Verify order updated notification
7. Validate updated order details

**Validations**:
- Edit confirmation modal shows correct modifications
- Order updated notification appears
- Modified order displays updated SL/TP values

---

### TC03: Modify Order With Partial SL/TP (`test_TRD_STPLMT_TC03_positive_modify_order_placed_with_sl_or_tp.py`)

**Purpose**: Tests modification of orders that have either SL or TP (but not both)

**Test Scenarios**:
- Order with SL=0: Update SL only
- Order with SL=0: Update TP only  
- Order with SL=0: Update both SL and TP
- Order with TP=0: Update SL only
- Order with TP=0: Update TP only
- Order with TP=0: Update both SL and TP

**Test Flow**:
1. Place order with one parameter set to 0 (SL or TP)
2. Verify order placement
3. Modify order with specified updates
4. Verify edit confirmation
5. Confirm update
6. Verify update notification
7. Validate final order state

**Validations**:
- Partial SL/TP orders can be successfully modified
- All update combinations work correctly
- Order details reflect the modifications

---

### TC04: Modify Order With Full SL/TP (`test_TRD_STPLMT_TC04_positive_modify_order_placed_with_sl_and_tp.py`)

**Purpose**: Tests modification of orders that already have both SL and TP configured

**Test Scenarios**:
- Update both SL and TP to POINTS type
- Update both SL and TP to PRICE type
- Update both SL and TP to random sample values

**Test Flow**:
1. Place order with both SL and TP
2. Verify order placement
3. Modify order with new SL/TP types
4. Verify edit confirmation
5. Confirm update
6. Verify update notification
7. Validate updated order details

**Validations**:
- Orders with existing SL/TP can be modified
- Different SL/TP type combinations work
- Updated values are correctly applied

---

### TC05: Delete Stop Limit Order (`test_TRD_STPLMT_TC05_positive_delete_order.py`)

**Purpose**: Validates successful deletion of pending stop limit orders

**Test Flow**:
1. Get current pending orders count
2. Place stop limit order
3. Verify order placement
4. Delete the pending order
5. Verify deletion notification
6. Verify pending orders count returns to original
7. Verify order no longer appears in list

**Validations**:
- Delete operation completes successfully
- Deletion notification appears
- Pending orders count decrements correctly
- Order is removed from pending orders list

---

### TC07: Cancel Order Placement (`test_TRD_STPLMT_TC07_positive_cancel_place_order.py`)

**Purpose**: Tests cancellation of order placement before confirmation

**Test Flow**:
1. Get current pending orders count
2. Initiate stop limit order placement
3. Cancel the trade confirmation modal
4. Verify pending orders count unchanged

**Validations**:
- Order placement can be cancelled
- No order is created when cancelled
- Pending orders count remains unchanged

---

### TC08: API Data Validation - Place Order (`test_TRD_STPLMT_TC08_positive_place_order_compare_against_api_data.py`)

**Purpose**: Validates that UI-placed orders match backend API data

**Test Flow**:
1. Get current pending orders count
2. Place stop limit order via UI
3. Verify pending orders count increased
4. Get order ID from UI
5. Fetch order details via API
6. Compare UI data against API response

**Validations**:
- UI and API data consistency
- Order details match between frontend and backend
- API integration works correctly

---

### TC09: API Data Validation - Modify Order (`test_TRD_STPLMT_TC09_positive_modify_order_compare_against_api_data.py`)

**Purpose**: Validates that UI-modified orders match backend API data

**Test Flow**:
1. Place stop limit order
2. Verify order placement
3. Modify order with SL, TP, and expiry
4. Verify modification in UI
5. Fetch updated order via API
6. Compare UI data against API response

**Validations**:
- Modified order data consistency between UI and API
- All modification parameters are correctly synchronized
- Backend properly reflects UI changes

## Key Testing Patterns

### Parameterized Testing
- Extensive use of `@pytest.mark.parametrize` for testing multiple scenarios
- SL/TP type combinations (PRICE, POINTS, random values)
- Different modification scenarios

### Test Data Management
- `stop_limit_obj` fixture provides consistent test data
- `create_order_data` fixture handles order creation
- `cancel_all` fixture ensures clean test environment

### Validation Strategies
- **UI Validations**: Modal confirmations, notification banners, tab counts
- **Data Validations**: Order details, SL/TP values, order states
- **API Validations**: Backend data consistency checks

### Test Markers
- `@pytest.mark.critical`: High-priority test cases
- Strategic marking of essential functionality tests

## Coverage Areas

### Functional Coverage
- ✅ Order placement with various SL/TP configurations
- ✅ Order modification scenarios (add, update, remove SL/TP)
- ✅ Order deletion functionality
- ✅ Order placement cancellation
- ✅ UI-API data consistency

### Edge Cases
- ✅ Orders without SL/TP
- ✅ Orders with partial SL/TP (one parameter = 0)
- ✅ Orders with full SL/TP configuration
- ✅ Different SL/TP types (PRICE vs POINTS)

### Integration Testing
- ✅ UI-API data synchronization
- ✅ Backend order management validation
- ✅ Real-time order state updates

## Test Dependencies

### Required Fixtures
- `web_app`: Web application instance
- `stop_limit_obj`: Stop limit order object factory
- `create_order_data`: Order creation helper
- `cancel_all`: Test cleanup
- `get_asset_tab_amount`: Tab count helper

### External Dependencies
- `APIClient`: Backend API integration
- `AssetTabs`: UI tab management
- `SLTPType`: Stop Loss/Take Profit type enums
- `OrderType`: Order type definitions

## Conclusion

The stop limit test suite provides comprehensive coverage of stop limit order functionality, ensuring robust validation of:
- Complete order lifecycle (place, modify, delete)
- Various SL/TP configurations and modifications
- UI-API data consistency
- Error handling and edge cases

This test suite follows automation best practices with parameterized testing, proper fixtures, and comprehensive validation strategies to ensure the reliability of the stop limit trading functionality.