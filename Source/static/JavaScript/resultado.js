$(document).ready(function(){
  $(".btnVolver").click(volver);

  function volver(){
    document.getElementById("formVolver").submit();
  }
});
