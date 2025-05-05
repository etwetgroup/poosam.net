var menus = [];
var submenus = [];
$( document ).ready(function() {
    $.ajax({
        type: "POST",
        url: "/mainMenuParentDataSource/",
        success: function(response_menu) {
            menus = response_menu;

            $.ajax({
                type: "POST",
                url: "/mainSubMenuDatasource/",
                success: function (response_submenu) {
                    submenus = response_submenu;
                },
            });

            $(() => {
              $('#gridContainer').dxDataGrid({
                dataSource: menus,
                keyExpr: 'ID',
                rtlEnabled: true,
                paging: {
                  pageSize: 15,
                },
                // filterRow: { visible: true },
                // filterPanel: { visible: true },
                // headerFilter: { visible: true },
                searchPanel: { visible: true },
                rowDragging: {
                  allowReordering: true,
                  onReorder(e) {
                    const visibleRows = e.component.getVisibleRows();
                    const toIndex = menus.findIndex((item) => item.ID === visibleRows[e.toIndex].data.ID);
                    const fromIndex = menus.findIndex((item) => item.ID === e.itemData.ID);

                    menus.splice(fromIndex, 1);
                    menus.splice(toIndex, 0, e.itemData);

                    data = {
                        table: 'mainmenu',
                        result: JSON.stringify(menus)
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
                        url: "/mainMenuDelete/" + e.data.ID,
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
                    dataField: 'title',
                    caption: 'عنوان منوهای اصلی',
                  },
                  {
                    type: 'buttons',
                    width: 150,
                    buttons: [{
                      hint: 'افزودن زیر منو',
                      icon: 'add',
                      onClick(e) {
                        // $("#txt_submenu").text(e.row.data.title);
                        // $('#modalAddSubMenus').modal('show');
                        // $("#pk_id_insert").val(e.row.data.ID);
                         window.location.href = '/subMenuAdd/' + e.row.data.ID + '/' ;
                      },
                    }, {
                      hint: 'ویرایش',
                      icon: 'edit',
                      onClick(e) {
                        // console.log(e.row.data.ID);
                        // $("#pk_id_edit").val(e.row.data.ID);
                        // $("#txt_edit_menu").text('ویرایش منوی اصلی');
                        //
                        // $.ajax({
                        //     type: "GET",
                        //     url: "/mainMenuEdit/",
                        //     data: {pk: e.row.data.ID},
                        //     dataType: 'json',
                        //     success: function (data) {
                        //         $("#title").val(data[0].title);
                        //         $("#titleseo").val(data[0].titleseo);
                        //         $("#keywords").tagsinput('add', data[0].keywords);
                        //         $("#desc").val(data[0].description);
                        //         $("#canonical").val(data[0].canonical);
                        //         CKEDITOR.instances['edit_text'].setData(data[0].text);
                        //         if (data[0].noindex)
                        //             $('#noindex').prop("checked", true);
                        //         if (data[0].showCmnt)
                        //             $('#showCmnt').prop("checked", true);
                        //     },
                        //     error: function (data) {
                        //
                        //     }
                        // });
                        // $('#modalEditMenus').modal('show');
                          window.location.href = '/menuEdit/' + e.row.data.ID + '/';
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
                            url: "/changeMainMenuActive/" + e.row.data.ID,
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
                            url: "/changeMainMenuActive/" + e.row.data.ID,
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
                      .addClass('master-detail-caption')
                      .text(` زیر منوهای : ${currentEmployeeData.title}`)
                      .appendTo(container);

                    $('<div>')
                      .dxDataGrid({
                        columnAutoWidth: true,
                        rowDragging: {
                          allowReordering: true,
                          onReorder(e) {
                            const visibleRows = e.component.getVisibleRows();
                            const toIndex = submenus.findIndex((item) => item.ID === visibleRows[e.toIndex].data.ID);
                            const fromIndex = submenus.findIndex((item) => item.ID === e.itemData.ID);

                            submenus.splice(fromIndex, 1);
                            submenus.splice(toIndex, 0, e.itemData);

                            data = {
                                table: 'mainmenu',
                                result: JSON.stringify(submenus)
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
                                url: "/mainMenuDelete/" + e.data.ID,
                                success: function(data) {
                                  // $("#gridContainer").dxDataGrid("instance").refresh();
                                  // location.reload();
                                  e.component.refresh();
                                }
                            });
                        },
                        showBorders: true,
                        rtlEnabled: true,
                        paging: {
                          pageSize: 15,
                        },
                        editing: {
                          // mode: 'popup',
                          allowUpdating: false,
                          allowDeleting: true,
                          allowAdding: false,
                        },
                        columns: [
                          {
                            dataField: 'title',
                            caption: 'عنوان زیر منوها',
                          },
                          {
                            type: 'buttons',
                            width: 150,
                            buttons: [{
                              hint: 'افزودن زیر منو',
                              icon: 'add',
                              onClick(e) {
                                // $("#txt_submenu").text(e.row.data.title);
                                // $('#modalAddSubMenus').modal('show');
                                // $("#pk_id_insert").val(e.row.data.ID);
                                  window.location.href = '/subMenuAdd/' + e.row.data.ID + '/' ;
                              },
                            }, {
                              hint: 'ویرایش',
                              icon: 'edit',
                              onClick(e) {
                                // console.log(e.row.data.ID);
                                // $("#pk_id_edit").val(e.row.data.ID);
                                // $("#txt_edit_menu").text('ویرایش زیر منو');
                                //
                                // $.ajax({
                                //     type: "GET",
                                //     url: "/mainMenuEdit/",
                                //     data: {pk: e.row.data.ID},
                                //     dataType: 'json',
                                //     success: function (data) {
                                //         $("#title").val(data[0].title);
                                //         $("#titleseo").val(data[0].titleseo);
                                //         $("#keywords").tagsinput('add', data[0].keywords);
                                //         $("#desc").val(data[0].description);
                                //         $("#canonical").val(data[0].canonical);
                                //         CKEDITOR.instances['edit_text'].setData(data[0].text);
                                //         if (data[0].noindex)
                                //             $('#noindex').prop("checked", true);
                                //         if (data[0].showCmnt)
                                //             $('#showCmnt').prop("checked", true);
                                //     },
                                //     error: function (data) {
                                //
                                //     }
                                // });
                                // $('#modalEditMenus').modal('show');
                                  window.location.href = '/subMenuEdit/' + e.row.data.ID + '/' ;
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
                                    url: "/changeMainMenuActive/" + e.row.data.ID,
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
                                    url: "/changeMainMenuActive/" + e.row.data.ID,
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
                      .addClass('master-detail-caption')
                      .text(` زیر منوهای : ${currentEmployeeData.title}`)
                      .appendTo(container);

                    $('<div>')
                      .dxDataGrid({
                        columnAutoWidth: true,
                        rowDragging: {
                          allowReordering: true,
                          onReorder(e) {
                            const visibleRows = e.component.getVisibleRows();
                            const toIndex = submenus.findIndex((item) => item.ID === visibleRows[e.toIndex].data.ID);
                            const fromIndex = submenus.findIndex((item) => item.ID === e.itemData.ID);

                            submenus.splice(fromIndex, 1);
                            submenus.splice(toIndex, 0, e.itemData);

                            data = {
                                table: 'mainmenu',
                                result: JSON.stringify(submenus)
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
                                url: "/mainMenuDelete/" + e.data.ID,
                                success: function(data) {
                                  // $("#gridContainer").dxDataGrid("instance").refresh();
                                  // location.reload();
                                  e.component.refresh();
                                }
                            });
                        },
                        showBorders: true,
                        rtlEnabled: true,
                        paging: {
                          pageSize: 15,
                        },
                        editing: {
                          // mode: 'popup',
                          allowUpdating: false,
                          allowDeleting: true,
                          allowAdding: false,
                        },
                        columns: [
                          {
                            dataField: 'title',
                            caption: 'عنوان زیر منو ها',
                          },
                          {
                            type: 'buttons',
                            width: 110,
                            buttons: [{
                              hint: 'ویرایش',
                              icon: 'edit',
                              onClick(e) {
                                // console.log(e.row.data.ID);
                                // $("#pk_id_edit").val(e.row.data.ID);
                                // $("#txt_edit_menu").text('ویرایش زیر منو');
                                // $.ajax({
                                //     type: "GET",
                                //     url: "/mainMenuEdit/",
                                //     data: {pk: e.row.data.ID},
                                //     dataType: 'json',
                                //     success: function (data) {
                                //         $("#title").val(data[0].title);
                                //         $("#titleseo").val(data[0].titleseo);
                                //         $("#keywords").tagsinput('add', data[0].keywords);
                                //         $("#desc").val(data[0].description);
                                //         $("#canonical").val(data[0].canonical);
                                //         CKEDITOR.instances['edit_text'].setData(data[0].text);
                                //         if (data[0].noindex)
                                //             $('#noindex').prop("checked", true);
                                //         if (data[0].showCmnt)
                                //             $('#showCmnt').prop("checked", true);
                                //     },
                                //     error: function (data) {
                                //
                                //     }
                                // });
                                // $('#modalEditMenus').modal('show');
                                  window.location.href = '/subMenuEdit/' + e.row.data.ID + '/' ;
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
                                    url: "/changeMainMenuActive/" + e.row.data.ID,
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
                                    url: "/changeMainMenuActive/" + e.row.data.ID,
                                    success: function(data) {
                                      location.reload();
                                    }
                                });
                              },
                            }, 'delete'],
                          },
                        ],
                        dataSource: new DevExpress.data.DataSource({
                          store: new DevExpress.data.ArrayStore({
                            key: 'ID',
                            data: submenus,
                          }),
                          filter: ['sub_menu_id', '=', options.key],
                        }),
                      }).appendTo(container);
                  },
                },
                        dataSource: new DevExpress.data.DataSource({
                          store: new DevExpress.data.ArrayStore({
                            key: 'ID',
                            data: submenus,
                          }),
                          filter: ['sub_menu_id', '=', options.key],
                        }),
                      }).appendTo(container);
                  },
                },
              });
            });
        }
    });
});

