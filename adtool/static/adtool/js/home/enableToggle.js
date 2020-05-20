function toggleEnabler(key, id, value) {
    clean_id = id.split('ad-id-')[1];
    en_button = document.getElementById(id);
    en_status = document.getElementById("ad-status-" + clean_id);
    $.ajax({
        type: "GET",
        url: "home/advertisement-enable-toggle-ajax/",
        data:{
            ad_id: clean_id,
            ad_key: key
        },
        success: function (data) {
            if (value === 'True') {
                en_button.innerHTML = "Click to enable";
                en_button.value = 'False';
                en_button.classList.remove('btn-success');
                en_button.classList.add('btn-secondary');
                en_status.innerHTML = 'status: Disabled';
            }
            else {
                en_button.innerHTML = "Click to disable";
                en_button.value = 'True';
                en_button.classList.remove('btn-secondary');
                en_button.classList.add('btn-success');
                en_status.innerHTML = 'status: Enabled';
            }
        },
    })
}