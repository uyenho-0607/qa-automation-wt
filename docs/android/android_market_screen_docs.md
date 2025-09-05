# Android Market Screen Documentation

## MarketsScreen Business Logic Features

### **Core Navigation & Tab Management**
• **Multi-tab watchlist interface** - Supports navigation between different market categories (All, Favourites, Top Picks, Top Gainer, Top Loser, Commodities, Crypto, Forex, Index, Shares)
• **Horizontal scroll tab handling** - Automatically scrolls horizontally to reveal hidden tabs when they're not immediately visible
• **Dynamic tab selection** - Intelligently handles both parent tabs and sub-tabs with fallback navigation logic

### **Symbol Management & Favorites**
• **Star/Unstar functionality** - Users can mark symbols as favorites or remove them from favorites list
• **Favorite symbol persistence** - Starred symbols appear in the Favourites tab across different screens
• **Random symbol selection** - Supports selecting random symbols from any watchlist for testing purposes
• **Symbol removal via swipe gesture** - Users can swipe left on symbols in Favourites tab to remove them

### **Symbol Preference & Filtering**
• **Granular symbol visibility control** - Users can show/hide specific symbols within each market category
• **Show All toggle** - Master control to display all symbols or apply custom filters
• **Persistent preference settings** - Symbol preferences are saved and applied across sessions
• **Bulk preference management** - Ability to modify multiple symbol preferences simultaneously

### **Watchlist Display & Interaction**
• **Symbol list retrieval** - Fetches and displays current symbols in selected tabs
• **Infinite scroll support** - Handles scrolling through large symbol lists with intelligent scroll detection
• **Symbol selection navigation** - Clicking on symbols redirects to detailed trade/chart view
• **Real-time symbol verification** - Validates symbol presence/absence in specific tabs

### **Cross-Screen Integration**
• **Seamless navigation flow** - Integrates with Trade screen for symbol selection and trading actions
• **Shared watchlist component** - Uses common WatchList component for consistent behavior across screens
• **API integration** - Connects with backend APIs for starring/unstarring symbols and preference management

### **User Experience Features**
• **Loading state handling** - Implements appropriate wait times for symbol list loading and tab transitions
• **Error handling** - Graceful handling of scroll limits and missing symbols
• **Visual feedback** - Provides confirmation messages for successful preference saves
• **Responsive design** - Adapts to different screen sizes and orientations

### **Test Coverage Areas**
• **TC01**: Star/Unstar symbol functionality and cross-tab verification
• **TC02**: Symbol preference management with show/hide capabilities  
• **TC03**: Symbol selection and navigation flow across all watchlist tabs

## Summary
The MarketsScreen serves as a comprehensive market data hub that allows users to organize, filter, and interact with financial instruments across multiple asset categories while maintaining personalized preferences and seamless navigation to trading functionality.