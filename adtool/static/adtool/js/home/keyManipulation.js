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

$( "#remove-key-modal" ).on("shown.bs.modal", function (e) { 
    const id = e.relatedTarget.id
    $( '#confirm-key-delete' ).attr('value', id);
    const cleanValue = id.split('delete-button-')[1];
    $( '#key-delete-displayer' ).html($( '#td-url-' + cleanValue ).text() + "<br />" + $('#td-' + cleanValue ).text() );
});
$( "#remove-key-modal" ).on("hidden.bs.modal", function (e) { 
    $( '#confirm-key-delete' ).removeAttr('value');
});

$( '#confirm-key-delete' ).on('click', function (e) {
    const cleanValue = $( '#confirm-key-delete' ).attr('value').split('delete-button-')[1];
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
    $( "#remove-key-modal" ).modal('hide')
})


// function deleteKey(value) {
//     const cleanValue = value.split('delete-button-')[1];
//     $.ajax(
//        { 
//             type: 'GET',
//            url: 'delete-userkey/',
//            data: {
//                key: cleanValue
//            },
//            success: function (data) {
//                $( '#tr-' + cleanValue ).remove();
//            }
//        }
//     );
// }