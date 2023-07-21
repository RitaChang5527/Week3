//*設定promotions顯示的地方
function displayPromotions(promotions) {
    //*取得promotions的ID
    var promotionsDiv = document.getElementById("promotions");
    //*promotion只顯示三個
    for (var i = 0; i < 3; i++) {
      //*創建圖片的<div>
      var promotionDiv = document.createElement("div");
      //*這個div的名字是promotion
      promotionDiv.className = "promotion";
  
      //* 切除網址 從https切除
      //*網址會變成["",""://www.example.com/image.jpg"]
      var images = promotions[i].image.split("https");
      //*再將https加回去並選擇陣列排行第一個的網址
      var image = "https" + images[1];

      //*創建<img>
      var imageElement = document.createElement("img");
      //*放入照片
      imageElement.src = image;
      //*照片說明
      imageElement.alt = promotions[i].title;
      //*設定大小
      imageElement.width = 80;
      imageElement.height = 50;

      //*創建文字的<div>
      var promotionTextDiv = document.createElement("div");
      //*這個div的名字是promotion_text
      promotionTextDiv.className = "promotion_text";
      //*依序放入文字
      promotionTextDiv.textContent = promotions[i].title;

      //*將元件加入到父元素promotionDiv
      promotionDiv.appendChild(imageElement);
      promotionDiv.appendChild(promotionTextDiv);

      //*再將promotion加入到promotions
      promotionsDiv.appendChild(promotionDiv);
    }
  }
  //*宣告json檔
  var url = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json";
  
  fetch(url)//* 發送 HTTP GET 請求，url 是要獲取資源的網址
    .then(response => response.json())//* 將回應轉換為 JSON 格式
    .then(data => {
      //* 在這裡處理獲取到的資料
      //* 只取前 15 個景點資料
      var attractions = data.result.results.slice(0, 15); 
      var promotions = [];
  
      //* 取得前三個 attractions 的資料並加入 promotions 陣列中
      for (var i = 0; i < 3 && i < attractions.length; i++) {
        var title = attractions[i].stitle;
        //* 取得第一張照片的網址
        var images = attractions[i].file.split("https");
        var image = "https" + images[1];
  
        promotions.push({ title: title, image: image });
      }
  
      displayPromotions(promotions);
  
      //* 取得attractions的ID
      var attractionsDiv = document.getElementById("attractions");
      //*顯示下半部分 3-15
      for (var i = 3; i < attractions.length; i++) {
        //*設定名稱
        var name = attractions[i].stitle;
        var address = attractions[i].address;
  
        //* 切除網址 從https切除
        //*網址會變成["",""://www.example.com/image.jpg"]
        var images = attractions[i].file.split("https");
        var image = "https" + images[1];
        //*創建<div>
        var titleDiv = document.createElement("div");
        titleDiv.className = "title";
        //*創建圖片的<IMG>
        var imageElement = document.createElement("img");
        //*設定圖片
        imageElement.src = image;
        imageElement.alt = name;
        imageElement.width = 150;
        imageElement.height = 200;
        //*創建文字的<div>
        var titleTextDiv = document.createElement("div");
        //*名稱叫attraction_text
        titleTextDiv.className = "title_text";
        //*放入名稱
        titleTextDiv.textContent = name;
        
        //*將元件加入到父元素titleDiv
        titleDiv.appendChild(imageElement);
        titleDiv.appendChild(titleTextDiv);
        //*再將titleDiv加入到attractionsDiv
        attractionsDiv.appendChild(titleDiv);
      }
    })
    .catch(error => console.error("Error:", error));
  