class TablePaginationHandler {
    page = 1
    limit = 10
    subpageURL = ''
    tableID = ''
    columnCount = 0
    parameters = {}
    sort = ''
    callback = () => {}

    constructor(subpageURL, tableID, columnCount, parameters={}, callback=() => {}) {
        this.subpageURL = subpageURL
        this.tableID = tableID
        this.columnCount = columnCount
        this.parameters = parameters
        this.callback = callback
        this.loadPage()
    }

    loadPage(){
        
        const self = this; 
        const params = {
            page:self.page, 
            sort:self.sort,
            column_count: self.columnCount,
            ...self.parameters
        }
        params.limit = self.limit
        const params_url = new URLSearchParams(params).toString();
        $(`#${self.tableID}`).loadSubpage({
            url: `${self.subpageURL}?${params_url}`,
            is_table_column: self.columnCount,
            callback: self.callback
        })
    }

    nextPage() {
        this.page += 1
        this.loadPage()
    }

    prevPage() {
        this.page -= 1
        this.loadPage()
    }

    updateLimit(limit) {
        this.page = 1
        this.limit = limit
        this.loadPage()
    }

    sortPage(sort) {
        if(sort == '') return;
        if(this.sort.includes(sort)) sort = this.sort
        
        if(sort.includes('-')){
            sort = sort.replace('-', '')
        } else {
            sort = '-' + sort
        }
        
        this.sort = sort
        this.loadPage()
    }

}