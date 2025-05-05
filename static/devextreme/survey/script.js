var surveys = [];
$( document ).ready(function() {
    $.ajax({
        type: "POST",
        url: "/surveyDataSource/",
        success: function(response_faq) {
            surveys = response_faq;
            $(() => {
              $('#gridContainer').dxDataGrid({
                dataSource: surveys,
                keyExpr: 'ID',
                rtlEnabled: true,
                paging: {
                  pageSize: 25,
                },
                searchPanel: { visible: true },
                rowDragging: {
                  allowReordering: true,
                  onReorder(e) {
                    const visibleRows = e.component.getVisibleRows();
                    const toIndex = surveys.findIndex((item) => item.ID === visibleRows[e.toIndex].data.ID);
                    const fromIndex = surveys.findIndex((item) => item.ID === e.itemData.ID);

                    surveys.splice(fromIndex, 1);
                    surveys.splice(toIndex, 0, e.itemData);

                    data = {
                        table: 'survey',
                        result: JSON.stringify(surveys)
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
                        url: "/surveyDelete/" + e.data.ID,
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
                    dataField: 'description',
                    caption: 'دیدگاه های مطرح شده',
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
                            url: "/surveyEdit/" + e.row.data.ID,
                            dataType: 'json',
                            success: function (data) {
                                $("#fullname").val(data[0].fullname);
                                $("#mobile").val(data[0].mobile);
                                $("#email").val(data[0].email);
                                $("#desc").val(data[0].description);
                                $("#answer").val(data[0].answer);
                            },
                            error: function (data) {

                            }
                        });
                        $('#modalEditSurvey').modal('show');
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
                            url: "/changeSurveyActive/" + e.row.data.ID,
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
                            url: "/changeSurveyActive/" + e.row.data.ID,
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
                            caption: 'پاسخ دیدگاه انتخابی'
                          },
                        ],
                        dataSource: new DevExpress.data.DataSource({
                          store: new DevExpress.data.ArrayStore({
                            key: 'ID',
                            data: surveys,
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

