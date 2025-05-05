var details = [];
$( document ).ready(function() {
    $.ajax({
        type: "POST",
        url: "/productsDatasource/",
        success: function(response_menu) {
            details = response_menu;

            $(() => {
              $('#gridContainer').dxDataGrid({
                dataSource: details,
                keyExpr: 'ID',
                rtlEnabled: true,
                paging: {
                  pageSize: 50,
                },
                searchPanel: { visible: true },
                rowDragging: {
                  allowReordering: true,
                  onReorder(e) {
                    const visibleRows = e.component.getVisibleRows();
                    const toIndex = details.findIndex((item) => item.ID === visibleRows[e.toIndex].data.ID);
                    const fromIndex = details.findIndex((item) => item.ID === e.itemData.ID);

                    details.splice(fromIndex, 1);
                    details.splice(toIndex, 0, e.itemData);

                    data = {
                        table: 'products',
                        result: JSON.stringify(details)
                    }

                    $.ajax({
                        type: "POST",
                        url: "/saveOrder/",
                        dataType : "json",
                        data : data,
                    });

                    e.component.refresh();
                  }
                },
                onRowRemoving: function (e) {
                  $.ajax({
                        type: "POST",
                        url: "/productsDelete/" + e.data.ID,
                        success: function(data) {
                          e.component.refresh();
                        }
                    });
                },
                showBorders: true,
                editing: {
                  allowUpdating: false,
                  allowDeleting: true,
                  allowAdding: false,
                },
                columns: [
                  {
                    dataField: 'pages',
                    caption: 'گروه محصول',
                  }, {
                    dataField: 'title',
                    caption: 'عنوان محصول',
                  },
                  {
                    dataField: 'url_category',
                    caption: 'دسته بندی لینک',
                  },
                  {
                    type: 'buttons',
                    width: 150,
                    buttons: [{
                      hint: 'ویرایش',
                      icon: 'edit',
                      onClick(e) {
                        window.location.href = '/productsEdit/' + e.row.data.ID + '/' ;
                      },
                    }, {
                      hint: 'فعالیت',
                      icon: 'fa fa-eye',
                      visible(e) {
                        return e.row.data.active;
                      },
                      onClick(e) {
                          $.ajax({
                            type: "POST",
                            url: "/changeProductsActive/" + e.row.data.ID,
                            success: function(data) {
                              location.reload();
                            }
                        });
                      },
                    }, {
                      hint: 'فعالیت',
                      icon: 'fa fa-eye-slash',
                      visible(e) {
                        return !e.row.data.active;
                      },
                      onClick(e) {
                          $.ajax({
                            type: "POST",
                            url: "/changeProductsActive/" + e.row.data.ID,
                            success: function(data) {
                              location.reload();
                            }
                        });
                      },
                    }, 'delete'],
                  },
                ],
              });
            });
        }
    });
});

