var faqs = [];
$( document ).ready(function() {
    $.ajax({
        type: "POST",
        url: "/faqDataSource/",
        success: function(response_faq) {
            faqs = response_faq;

            $(() => {
              $('#gridContainer').dxDataGrid({
                dataSource: faqs,
                keyExpr: 'ID',
                rtlEnabled: true,
                paging: {
                  pageSize: 10,
                },
                searchPanel: { visible: true },
                rowDragging: {
                  allowReordering: true,
                  onReorder(e) {
                    const visibleRows = e.component.getVisibleRows();
                    const toIndex = faqs.findIndex((item) => item.ID === visibleRows[e.toIndex].data.ID);
                    const fromIndex = faqs.findIndex((item) => item.ID === e.itemData.ID);

                    faqs.splice(fromIndex, 1);
                    faqs.splice(toIndex, 0, e.itemData);

                    data = {
                        table: 'faq',
                        result: JSON.stringify(faqs)
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
                onRowRemoving: function (e) {
                  // console.log(e.data.ID);
                  $.ajax({
                        type: "POST",
                        url: "/faqDelete/" + e.data.ID,
                        success: function(data) {
                          // $("#gridContainer").dxDataGrid("instance").refresh();
                          // location.reload();
                          e.component.refresh();
                        }
                    });
                },
                showBorders: true,
                editing: {
                  // mode: 'popup',
                  allowUpdating: false,
                  allowDeleting: true,
                  allowAdding: false,
                },
                columns: [
                  {
                    dataField: 'question',
                    caption: 'سوالات مطرح شده',
                  },
                  {
                    type: 'buttons',
                    width: 150,
                    buttons: [{
                      hint: 'ویرایش',
                      icon: 'edit',
                      onClick(e) {
                        $("#pk_id_edit").val(e.row.data.ID);
                        $("#txt_edit_faq").text('ویرایش پرسش و پاسخ');

                        $.ajax({
                            type: "GET",
                            url: "/faqEdit/" + e.row.data.ID,
                            dataType: 'json',
                            success: function (data) {
                                $("#question").val(data[0].question);
                                $("#answer").val(data[0].answer);
                            },
                            error: function (data) {

                            }
                        });
                        $('#modalEditFaq').modal('show');
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
                            url: "/changeFaqActive/" + e.row.data.ID,
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
                            url: "/changeFaqActive/" + e.row.data.ID,
                            success: function(data) {
                              location.reload();
                            }
                        });
                      },
                    }, 'delete'],
                  },
                ],
                masterDetail: {
                  enabled: true,
                  template(container, options) {
                    const currentEmployeeData = options.data;
                    $('<div>')
                      .dxDataGrid({
                        columnAutoWidth: true,
                        showBorders: true,
                        rtlEnabled: true,
                        columns: [
                          {
                            dataField: 'answer',
                            caption: 'پاسخ سوال انتخابی'
                          },
                        ],
                        dataSource: new DevExpress.data.DataSource({
                          store: new DevExpress.data.ArrayStore({
                            key: 'ID',
                            data: faqs,
                          }),
                          filter: ['ID', '=', options.key],
                        }),
                      }).appendTo(container);
                  },
                },
              });
            });
        }
    });
});

