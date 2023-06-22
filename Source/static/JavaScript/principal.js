$(document).ready(function(){
  var EmptyfileList=$("#fileBrowse")[0].files;
  $(".btnDiagnosticar").click(upload);
  loadExternHTML();

  function upload(){

    var formData=new FormData(); //La imagen va aquí, en esta estructura.
    var file=$("#fileBrowse")[0].files; //Se obtiene la imagen.

    
    console.log(file);
    console.log(file.length);

    if(file.length==1){
      formData.append("tipo", "imagen");  //Se añade el tipo de peticion para poder ser gestionada mediante el controlador.
      formData.append("miFichero", file[0]); //Se añade el fichero, el nombre que aparece al comienzo es el que permitirá recuperar el mismo en el servidor.
      console.log(formData);

      $(".modal-loader").css("display", "block");
      $.ajax({
        type: 'POST',
        url: '/',
        data: formData,
        contentType: false, //De este modo no se añade el tipo de contenido en la cabecera.
        processData: false, //Incluyendo esta opción se evita que se combiertan los datos transferidos a texto puesto que no se desea que el fichero se convierta en texto.
        success: function(response){
          document.getElementById("btnResultado").submit();
        },
        error: function(error){
          console.log('Error: ', error);
          $(".modal-loader").css("display", "none");
          alert("Error al enviar la imagen");
        }
      });
    }
    else{
      alert("Debe subir una única imagen");
    }
  }
  //Permite cambiar la etiqueta al nombre del fichero (se lanza cuando se elige el fichero).
  $("#fileBrowse").change(verificarFichero);

  //Se lanza cuando se arrastra.
  $("#drop_zone").on("drop", function(event){
    event.preventDefault(); //Evitamos la acción por defecto cuando arrastras un elemento al navegador.
    $("#fileBrowse")[0].files=event.originalEvent.dataTransfer.files;  //Se asigna el fichero al input.
    verificarFichero();
  });

  //Cuando se arrastra un fichero dentro del cuadro donde se depositan.
  $("#drop_zone").on('dragover dragenter', function() {
    $(".boxUpload").css("background-color", "#0190af");
    $("#drop_zone").css("border-color", "#EEE");
    $("#drop_zone p").css("color", "white");
    $("#drop_zone i").css("color", "white");
  });

  //Cuando se suelta un fichero dentro del cuadro donde se depositan.
  $("#drop_zone").on('dragleave dragend drop', function() {
    $(".boxUpload").css("background-color", "#EEE");
    $("#drop_zone").css("border-color", "#0190af");
    $("#drop_zone p").css("color", "black");
    $("#drop_zone i").css("color", "#0190af");
  });

  function verificarFichero(){
    
    var file=$("#fileBrowse")[0].files;
    if(file[0]!=null){  //Se busca solucionar la excepción que se produce en chrome por llamar varias veces a verificarFichero generando las últimas excepción.
      var extension= getFileExtension(file[0].name);

      if(extension=="jpg" || extension=="JPG" || extension=="PNG" || extension=="png" || extension=="jpeg" || extension=="JPEG"){  //Comprobamos que la extensión se corresponda con las existentes.
        $(".inputNameFile").text(file[0].name);
        $("#drop_zone p").text(file[0].name);
        $(".inputNameFile").prepend('<i class="far fa-file-image" style="font-size:24px;color:#0190af;margin-right:10px;"></i>');
        $("#drop_zone p").prepend('<i class="far fa-file-image" style="font-size:48px;color:#0190af;margin-right:10px;">');
      }
      else{
        $(".inputNameFile").text("Nombre de la imagen");
        $("#drop_zone p").text("Arrastrar imagen aquí");
        $(".inputNameFile").prepend('<i class="far fa-file-image" style="font-size:24px;color:#0190af;margin-right:10px;"></i>');
        $("#drop_zone p").prepend('<i class="fa fa-download" style="font-size:48px;color:#0190af">');
        $("#fileBrowse")[0].files=EmptyfileList;  //Vaciamos la lista de imagenes.
        alert("Error  extensión invalida");
      }
    }
  }

  function getFileExtension(cadena){
    aux=cadena.split("."); //Se obtiene la extensión del fichero.
    if (aux.length>=2){
      return aux[aux.length-1];  //Se devuelve la extensión.
    }
    else{
      return ""; //Se devuelve una cadena vacía si no tiene extensión.
    }
  }

  //Permite cargar las ventanas externas (HTML externo).
  function loadExternHTML(){
    $("#ContenedorSecundario").load("../static/StaticHTML/Cargando.html");
  }
});