# Filter Page Implementation

Implement a comprehensive product filtering page for the product price monitoring dashboard with advanced filtering capabilities.

## Instructions

1. **Backend API Enhancement**
   - Extend `/products` endpoint in `src/product_prices/api/routes.py` with new filter parameters:
     * `category`: Product type filtering (t-shirt, sweatshirt, hoodie, jacket, pants)
     * `min_price`/`max_price`: Price range filtering
     * `on_sale`: Boolean for discounted items only
     * `search`: Text search in product names
   - Add category detection logic using regex patterns:
     * T-Shirt: `/t-shirt|tee|tshirt/i`
     * Sweatshirt/Hoodie: `/sweat|hoodie|hooded/i`
     * Jacket: `/jacket|coat/i`
     * Pants: `/pant|trouser|jean/i`
   - Implement proper SQL query building with parameterized queries
   - Add error handling and validation for all new parameters
   - **Quality Gate**: Test API endpoints with various filter combinations

2. **Frontend Navigation Setup**
   - Update `dashboard/app/layout.tsx` to include navigation header
   - Add links to main dashboard (`/`) and new filter page (`/filter`)
   - Ensure consistent styling with existing gradient design system
   - Use Tailwind CSS classes matching current theme (blue/purple gradients)
   - **Quality Gate**: Verify navigation works and styling is consistent

3. **Filter Page Implementation**
   - Create `dashboard/app/filter/page.tsx` with comprehensive filtering interface:
     * Multi-select source filtering (tony_mcdonald, carhartt_wip, end_clothing)
     * Category filter buttons for product types
     * Price range dual slider component
     * "Sale Items Only" toggle switch
     * Stock status filtering (in stock/out of stock/all)
     * Search bar with real-time filtering and debounce
     * Sort options (price low/high, discount %, newest/oldest)
   - Implement URL state persistence using Next.js router
   - Add loading states with skeleton components
   - Include error handling with user-friendly messages
   - **Quality Gate**: Ensure all filters work independently and in combination

4. **Reusable Filter Components**
   - Create `dashboard/components/product-filter.tsx`:
     * Collapsible filter sections
     * Filter state management with React hooks
     * Clear filters functionality
     * Filter count badges
   - Create `dashboard/components/filtered-product-grid.tsx`:
     * Responsive grid layout (1-4 columns based on screen size)
     * Product cards with enhanced information display
     * Pagination component (20 items per page)
     * Grid/list view toggle
     * Empty state when no products match filters
   - **Quality Gate**: Test components are reusable and responsive

5. **Type System and API Updates**
   - Extend `dashboard/lib/types.ts` with new interfaces:
     ```typescript
     interface ProductFilters {
       sources?: string[]
       categories?: string[]
       minPrice?: number
       maxPrice?: number
       onSale?: boolean
       inStock?: boolean | null
       search?: string
       sortBy?: 'price_asc' | 'price_desc' | 'discount_desc' | 'newest' | 'oldest'
       page?: number
       limit?: number
     }

     interface FilteredProductsResponse {
       products: ProductResponse[]
       total: number
       page: number
       totalPages: number
       appliedFilters: ProductFilters
     }
     ```
   - Update `dashboard/lib/api.ts` with new functions:
     * `getFilteredProducts(filters: ProductFilters)`
     * `getProductCategories()`
     * `getFilterStats()` for showing counts per filter option
   - **Quality Gate**: Ensure TypeScript compilation passes without errors

6. **Advanced Features Implementation**
   - Add filter persistence in localStorage for user convenience
   - Implement filter URL sharing (users can bookmark filtered views)
   - Add "Recently Viewed Filters" section
   - Include filter analytics (track most used filters)
   - Add export functionality for filtered results (CSV format)
   - **Quality Gate**: Test advanced features work across browser sessions

7. **Performance Optimization**
   - Implement debounced search to avoid excessive API calls
   - Add client-side caching for filter options
   - Use React.memo for filter components to prevent unnecessary re-renders
   - Implement virtual scrolling for large product lists
   - Add loading indicators for slow operations
   - **Quality Gate**: Verify page loads quickly and feels responsive

8. **Mobile Responsiveness**
   - Create mobile-optimized filter drawer/modal
   - Implement touch-friendly filter controls
   - Ensure product grid adapts to mobile screens
   - Add swipe gestures for navigation
   - Test on various screen sizes (mobile, tablet, desktop)
   - **Quality Gate**: Confirm excellent mobile experience

9. **Integration Testing**
   - Test filter page with all three data sources (tony_mcdonald, carhartt_wip, end_clothing)
   - Verify filtering works with different product types
   - Test edge cases (no results, API errors, network issues)
   - Ensure proper error boundaries and fallback states
   - Validate accessibility (keyboard navigation, screen readers)
   - **Quality Gate**: Complete end-to-end testing passes

10. **Documentation and Polish**
    - Add inline code comments for complex filtering logic
    - Update project README with filter page documentation
    - Create user guide for filter functionality
    - Add analytics tracking for filter usage
    - Implement proper SEO meta tags for filter page
    - **Quality Gate**: Code is well-documented and production-ready

## Expected Deliverables

- Enhanced API endpoint supporting 8+ filter parameters
- Complete filter page with 10+ filtering options
- 2 reusable React components for filtering
- Mobile-responsive design matching existing theme
- URL state persistence and sharing capabilities
- Export functionality for filtered data
- Comprehensive error handling and loading states

## Success Criteria

- Users can filter 657+ products by multiple criteria simultaneously
- Page loads in under 2 seconds with smooth interactions
- Mobile experience is touch-friendly and intuitive
- All filters work independently and in combination
- Filter state persists across browser sessions
- API handles large datasets efficiently with pagination
