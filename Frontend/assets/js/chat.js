var sdk = apigClientFactory.newClient();

// for upload
var name = '';
var outerHtml = null;
var fileExt = null;


// function for searching image
function searchImage() {
  searchText = document.getElementById('searchText').value
  console.log(searchText)
  document.getElementById("displayImage").innerHTML = null;

  if (searchText == "") {
    alert("Empty string provided to search");
  } else {
    var params = { "q": searchText };
    var body = {}
    var additionalParams = {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'X-Api-Key': 'b982NROVVT6Y0LCoaWprbtqZilFZzSH5rxEIwxn9'
      }
    }
    //var additionalParams = {}
    sdk.searchGet(params, body, additionalParams).then(function(response) {
      console.log(response)
      if (response['data']['body'] == '') {
        alert("no image found")
      } else {
        var displayImage = document.getElementById("displayImage")
        var allImages = JSON.parse(response['data']['body']);
        for(var i =0;i<allImages.length;++i) {
          var img = new Image();
          img.src = allImages[i];
          displayImage.appendChild(img);
        }
      }
      // write code for response once we know what the response is
    }).catch(function (result) {
      alert("error searching data")
    });
  }
}

// function to view image
function viewImage(image) {
  globalVarImageFile = null;
  bodyForImageToUpload = null;
  console.log(image)
  console.log(image.files)
  var reader = new FileReader();
  name = image.files[0].name;
  fileExt = name.split(".").pop();
  var nameWithoutExtension = name.replace(/\.[^/.]+$/, "");
  var finalName = nameWithoutExtension + "_" + Date.now() + "." + fileExt;
  name = finalName;

  reader.onload = function (event) {
    console.log(event)
    var src = event.target.result;
    var newImage = document.createElement("img");
    newImage.src = src;
    outerHtml = newImage.outerHTML;
  }
  reader.readAsDataURL(image.files[0]);
}

// function to upload
function uploadImage() {
  var files = document.getElementById("imgId").files;

  if (!files.length) {
    return alert("Please choose a file to upload first.");
  }

  var file = files[0];
  var fileName = file.name;
  console.log("File:", file);
  console.log("File type:", file.type);
  last_index_quote = outerHtml.lastIndexOf('"');
  if (fileExt == 'jpg' || fileExt == 'jpeg') {
    body = outerHtml.substring(33, last_index_quote);
    filetype = "image/jpeg" + ";base64"
  }
  else {
    body = outerHtml.substring(32, last_index_quote);
    filetype = file.type + ";base64"
  }
  var customLabel = document.getElementById('customLabels').value; 
  console.log(customLabel);
  var params = {
    'key': fileName,
    'Content-Type': filetype,
    'bucket': 'photoalbumassignment2storingphotoctsn',
    //,'Metadata': {'x-amz-meta-customlabels':customLabel}
    //,'Metadata': {'customlabels':customLabel}
    'x-amz-meta-customlabels':customLabel,
    'Access-Control-Allow-Origin': '*',
    //,'customlabels':customLabel
  };
  console.log("Params are ", params);
  var additionalParams = {
    headers: {
      'Content-Type': filetype,
      'Access-Control-Allow-Origin': '*',
      'X-Api-Key': 'b982NROVVT6Y0LCoaWprbtqZilFZzSH5rxEIwxn9'//,
      //,'x-amz-meta-customlabels':''
      //'x-amz-meta-customLabels':customLabel
    }
  }

  sdk.uploadBucketKeyPut(params, body, additionalParams).then(function (result) {
    console.log("Uploaded image successfully");
    alert("Uploaded image successfully");
    console.log(result);
  }).catch(function (err) {
    alert("Failed to upload image");
  });
}
