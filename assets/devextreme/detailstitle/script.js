var details = [];
$( document ).ready(function() {
    $.ajax({
        type: "POST",
        url: "/detailsTitleDatasource/",
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
                        table: 'detailsTitle',
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
                        url: "/detailsTitleDelete/" + e.data.ID,
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
                    caption: 'گروه جزییات',
                  }, {
                    dataField: 'title',
                    caption: 'عنوان جزییات',
                  },
                  {
                    type: 'buttons',
                    width: 150,
                    buttons: [{
                      hint: 'ویرایش',
                      icon: 'edit',
                      onClick(e) {
                        $("#pk_id_edit").val(e.row.data.ID);
                        $("#txt_edit_details").text('ویرایش عناوین جزییات');

                        $.ajax({
                            type: "GET",
                            url: "/detailsTitleEdit/",
                            data: {pk: e.row.data.ID},
                            dataType: 'json',
                            success: function (data) {
                                $("#title").val(data[0].title);
                                $("#page").val(data[0].pages_id);
                            },
                            error: function (data) {

                            }
                        });
                        $('#modalEditDetailsTitle').modal('show');
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
                            url: "/changeDetailsTitleActive/" + e.row.data.ID,
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
                            url: "/changeDetailsTitleActive/" + e.row.data.ID,
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

