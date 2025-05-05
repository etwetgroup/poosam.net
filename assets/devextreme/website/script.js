var categories = [];
var sub_categories = [];
$( document ).ready(function() {
    $.ajax({
        type: "POST",
        url: "/websiteDataSource/",
        success: function(response) {
            categories = response;

            $.ajax({
                type: "POST",
                url: "/websiteSubDatasource/",
                success: function (response_sub) {
                    sub_categories = response_sub;
                },
            });

            $(() => {
              $('#gridContainer').dxDataGrid({
                dataSource: categories,
                keyExpr: 'ID',
                rtlEnabled: true,
                paging: {
                  pageSize: 10,
                },
                // filterRow: { visible: true },
                // filterPanel: { visible: true },
                // headerFilter: { visible: true },
                searchPanel: { visible: true },
                rowDragging: {
                  allowReordering: true,
                  onReorder(e) {
                    const visibleRows = e.component.getVisibleRows();
                    const toIndex = categories.findIndex((item) => item.ID === visibleRows[e.toIndex].data.ID);
                    const fromIndex = categories.findIndex((item) => item.ID === e.itemData.ID);

                    categories.splice(fromIndex, 1);
                    categories.splice(toIndex, 0, e.itemData);

                    data = {
                        table: 'website_category',
                        result: JSON.stringify(categories)
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
                onRowPrepared: function(e){
                  if(e.rowType == "data"){
                    e.rowElement.find(".dx-datagrid-group-closed").append("<i class='fa fa-plus' aria-hidden='true''></i>")
                    e.rowElement.find(".dx-datagrid-group-opened").append("<i class='fa fa-minus' aria-hidden='true''></i>")
                  }
                },
                showBorders: true,
                editing: {
                  // mode: 'popup',
                  allowUpdating: false,
                  allowDeleting: false,
                  allowAdding: false,
                },
                columns: [
                  {
                    dataField: 'title',
                    caption: 'عناوین',
                  },
                ],
                masterDetail: {
                  enabled: true,
                  template(container, options) {
                    const currentEmployeeData = options.data;

                    $('<div>')
                      .addClass('master-detail-caption')
                      .text(` متغیرهای : ${currentEmployeeData.title}`)
                      .appendTo(container);

                    $('<div>')
                      .dxDataGrid({
                        columnAutoWidth: true,
                        rowDragging: {
                          allowReordering: true,
                          onReorder(e) {
                            const visibleRows = e.component.getVisibleRows();
                            const toIndex = sub_categories.findIndex((item) => item.ID === visibleRows[e.toIndex].data.ID);
                            const fromIndex = sub_categories.findIndex((item) => item.ID === e.itemData.ID);

                            sub_categories.splice(fromIndex, 1);
                            sub_categories.splice(toIndex, 0, e.itemData);

                            data = {
                                table: 'website_category',
                                result: JSON.stringify(sub_categories)
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
                        showBorders: true,
                        rtlEnabled: true,
                        paging: {
                          pageSize: 10,
                        },
                        editing: {
                          mode: 'row',
                          allowUpdating: true,
                          allowDeleting: false,
                          allowAdding: false,
                        },
                        onRowUpdating: function (e) {
                           var id = e.key;
                           var title_value = e.newData.title_value;
                           var desc_value = e.newData.desc_value;

                           if (title_value === undefined)
                               title_value = ''

                           if (desc_value === undefined)
                               desc_value = ''

                           $.ajax({
                                type: "POST",
                                url: "/changeWebSite/",
                                data : {id: id,title_value: title_value,desc_value: desc_value},
                           });
                        },
                        columns: [
                          {
                            dataField: 'title_value',
                            caption: 'عنوان',
                          }, {
                            dataField: 'desc_value',
                            caption: 'ارزش',
                          },
                        ],
                        dataSource: new DevExpress.data.DataSource({
                          store: new DevExpress.data.ArrayStore({
                            key: 'ID',
                            data: sub_categories,
                          }),
                          filter: ['sub_category_id', '=', options.key],
                        }),
                      }).appendTo(container);
                  },
                },
              });
            });
        }
    });
});

