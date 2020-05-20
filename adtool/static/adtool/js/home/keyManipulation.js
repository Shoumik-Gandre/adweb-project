function changeKey(value) {
    const cleanValue = value.split('change-button-')[1];
     $.ajax(
        { 
            type: 'GET',
            url: 'change-userkey/',
            data: {
                key: cleanValue
            },
            success: function (data) {
                $( '#' + value ).attr('id', 'change-button-' + data);
                $( '#delete-button-' + cleanValue ).attr('id', 'delete-button-' + data);
                $( '#td-' + cleanValue ).attr('id', 'td-' + data);
                $( '#tr-' + cleanValue ).attr('id', 'tr-' + data)
                $( '#td-' + data ).text(data);
            }
        }
     );
}

function deleteKey(value) {
    const cleanValue = value.split('delete-button-')[1];
    $.ajax(
       { 
            type: 'GET',
           url: 'delete-userkey/',
           data: {
               key: cleanValue
           },
           success: function (data) {
               $( '#tr-' + cleanValue ).remove();
           }
       }
    );
}