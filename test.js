const jQuery = require('jQuery');
jQuery.ajax({
    type: "POST",
    url: 'your_functions_address.php',
    dataType: 'json',
    data: {functionname: 'add', arguments: [1, 2]},

    success: function (obj, textstatus) {
                  if( !('error' in obj) ) {
                      yourVariable = obj.result;
                  }
                  else {
                      console.log(obj.error);
                  }
            }
});
