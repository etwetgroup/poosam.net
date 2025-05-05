var users = [];
$( document ).ready(function() {
    $.ajax({
        type: "POST",
        url: "/userDataSource/",
        success: function(response) {
            users = response;

            $(() => {
              $('#gridContainer').dxDataGrid({
                dataSource: users,
                keyExpr: 'ID',
                rtlEnabled: true,
                paging: {
                  pageSize: 10,
                },
                searchPanel: { visible: true },
               onRowRemoving: function (e) {
                  $.ajax({
                        type: "POST",
                        url: "/userDelete/" + e.data.ID,
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
                    dataField: 'mobile',
                    caption: 'شماره همراه',
                  },
                  {
                    dataField: 'first_name',
                    caption: 'نام',
                  },
                  {
                    dataField: 'last_name',
                    caption: 'نام خانوادگی',
                  },
                  {
                    type: 'buttons',
                    width: 150,
                    buttons: [{
                      hint: 'ویرایش',
                      icon: 'edit',
                      onClick(e) {
                          window.location.href = '/userEdit/' + e.row.data.ID + '/';
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
                            url: "/changeUserActive/" + e.row.data.ID,
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
                            url: "/changeUserActive/" + e.row.data.ID,
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

