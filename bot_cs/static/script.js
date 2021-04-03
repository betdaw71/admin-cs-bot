var app = new Vue({
    el: "#app",
    data: {
        editor: false,
    },
    methods:{
        editorF(){
            this.editor = true;
            axios.get('/api/bots/')
            .then(response=>{
                this.events = response.data;
                console.log(response.data);
                setTimeout(function(){
                    for(var i=0;i<response.data.length;i++){
                        document.querySelector('#myTextarea').value += '["comments":"'+response.data[i].comment+'","login":"'+response.data[i].login+'","pass":"'+response.data[i].password+'","steamID":"'+response.data[i].steamid+'","shared_secret":"'+response.data[i].shared_secret+'","steamAPI":"'+response.data[i].steamAPI+'","googleDriveId":"'+response.data[i].googleDriveId+'","proxy":"'+response.data[i].proxy+'"]\n';
                    }
                },50)
            });
        },
        editorClose(){
            this.editor = false;
        },
        saveChanges(){
            document.querySelector('.formSave').submit();
        },
    },
    created(){
        console.log('asdasd');
    }
}); 

$('.checkBot').click(function(){
    if ($(this).is(':checked')){
        console.log('on'+$(this).data('login'));
        $.get('/boton/'+$(this).data('login'));
	} else {
		console.log('off'+$(this).data('login'));
        $.get('/botoff/'+$(this).data('login'));
	}
});
const selectSingle = document.querySelector('.__select');
const selectSingle_title = selectSingle.querySelector('.__select__title');
const selectSingle_labels = selectSingle.querySelectorAll('.__select__label');

// Toggle menu
selectSingle_title.addEventListener('click', () => {
  if ('active' === selectSingle.getAttribute('data-state')) {
    selectSingle.setAttribute('data-state', '');
  } else {
    selectSingle.setAttribute('data-state', 'active');
  }
});

// Close when click to option
for (let i = 0; i < selectSingle_labels.length; i++) {
  selectSingle_labels[i].addEventListener('click', (evt) => {
    selectSingle_title.textContent = evt.target.textContent;
    selectSingle.setAttribute('data-state', '');
  });
}

// Reset title
const reset = document.querySelector('.reset');
reset.addEventListener('click', () => {
  selectSingle_title.textContent = selectSingle_title.getAttribute('data-default');
});



$(function() {
  $('input[name="daterange"]').daterangepicker({
    opens: 'left'
  }, function(start, end, label) {
    console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
  });
    $('input[name="daterange1"]').daterangepicker({
    opens: 'left'
  }, function(start, end, label) {
    console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
  });
});
