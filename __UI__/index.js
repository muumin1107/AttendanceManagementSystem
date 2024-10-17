// DOMがロードされたら実行される処理
document.addEventListener('DOMContentLoaded', function() {
    updateDateTime();                // 現在日時を表示
    setInterval(updateDateTime, 1000); // 毎秒日時を更新
});

// 現在日時を更新する関数
function updateDateTime() {
    const now         = new Date();
    const dateOptions = {year: 'numeric', month: '2-digit', day: '2-digit'};
    const timeOptions = {hour: '2-digit', minute: '2-digit', second: '2-digit'};
    
    document.getElementById('currentDate').textContent = now.toLocaleDateString('ja-JP', dateOptions);
    document.getElementById('currentTime').textContent = now.toLocaleTimeString('ja-JP', timeOptions);
}

/* ------------------------------
   勤怠ボタン関連の処理
------------------------------ */

// ボタンクリック時の処理
function handleButtonClick(clickedButton) {
    _colorChange(clickedButton);  // ボタンの色を変更
    _moveCardUp();                // カードを上に移動
}

// ボタンの色を変更する関数
function _colorChange(clickedButton) {
    const buttons = document.querySelectorAll('.button-container button');

    // すべてのボタンを初期化
    buttons.forEach(button => _resetButtonColor(button));

    // クリックされたボタン以外をグレーに変更
    buttons.forEach(button => {
        if (button !== clickedButton) {
            button.style.backgroundColor = "#ccc";
            button.style.opacity = "0.7";
        }
    });
}

// ボタンの色をリセットする関数
function _resetButtonColor(button) {
    const defaultColors = {
        clockIn    : '#f44336',
        breakStart : '#4CAF50',
        breakEnd   : '#4CAF50',
        clockOut   : '#2196F3'
    };
    button.style.backgroundColor = defaultColors[button.id] || '#ccc';
    button.style.opacity = "1";
}

// カードを上に移動する関数
function _moveCardUp() {
    const card = document.getElementById('cardContainer');
    card.style.transform = 'translateY(-100px)';
}

/* ------------------------------
   モーダル関連の処理
------------------------------ */

// モーダルを開く
function openModal() {
    _initModal(); // モーダルを初期化

    const modalOverlay   = document.getElementById('modalOverlay');
    const modalContainer = document.getElementById('modalContainer');

    // モーダルを表示
    modalOverlay.classList.add('active');
    setTimeout(() => {
        modalContainer.classList.add('active');
    }, 10);

    // モーダル外をクリックしたら閉じる
    modalOverlay.addEventListener('click', function(event) {
        if (event.target === modalOverlay) {
            _closeModal();
        }
    });
}

// モーダルを初期化
function _initModal() {
    document.getElementById('fullName').value                  = '';
    document.getElementById('attribute').value                 = 'value';
    document.getElementById('description').value               = '';

    document.getElementById('name_error').style.display        = 'none';
    document.getElementById('attribute_error').style.display   = 'none';
    document.getElementById('description_error').style.display = 'none';
    document.getElementById('fullName').style.borderColor      = '#ccc';
    document.getElementById('attribute').style.borderColor     = '#ccc';
    document.getElementById('description').style.borderColor   = '#ccc';
}

// モーダルを閉じる
function _closeModal() {
    const modalOverlay   = document.getElementById('modalOverlay');
    const modalContainer = document.getElementById('modalContainer');
    
    modalContainer.classList.remove('active');
    setTimeout(() => {
        modalOverlay.classList.remove('active');
    }, 300);
}

/* ------------------------------
   登録処理関連
------------------------------ */

// 登録ボタンクリック時の処理
async function handleRegisterClick() {
    if (_validateForm()) {
        // フォームの入力値を取得
        const id = "test";
        const fullName = document.getElementById('fullName').value;
        const attribute = document.getElementById('attribute').value;
        const description = document.getElementById('description').value;

        // APIを呼び出して登録処理を行う
        const result = await _registerIDdata(id, fullName, attribute, description);
        if (result) {
            alert('登録しました');
        } else {
            alert('登録に失敗しました');
        }

        // モーダルを閉じる
        _closeModal();
    }
}

// IDデータを登録する関数
async function _registerIDdata(id, name, attribute, description) {
    const url = "https://fast-gnni-shizuokauniversity-8f675ed2.koyeb.app/register_id";
    const data = {
        id: id,
        name: name,
        attribute: attribute,
        description: description
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return response.ok;
    } catch (error) {
        console.error('IDデータ登録時に想定外のエラーが発生しました（以下，エラー内容）');
        console.error(error);
        return false;
    }
}


// フォームの入力値を検証する関数
function _validateForm() {
    const fullName          = document.getElementById('fullName').value.trim();
    const description       = document.getElementById('description').value.trim();
    const name_error        = document.getElementById('name_error');
    const name_input        = document.getElementById('fullName');
    const attribute_error   = document.getElementById('attribute_error');
    const attribute_input   = document.getElementById('attribute');
    const description_error = document.getElementById('description_error');
    const description_input = document.getElementById('description');

    let isValid = true;

    // 名前の検証（全角カタカナまたは漢字）
    const nameRegex = /^[\u30A0-\u30FF\u4E00-\u9FFF]+$/;
    if (!nameRegex.test(fullName)) {
        name_error.style.display = "block";
        name_input.style.borderColor = "red";
        isValid = false;
    } else {
        name_error.style.display = "none";
        name_input.style.borderColor = "#ccc";
    }

    // 属性の検証（選択されていること）
    var attribute_value = document.getElementById('attribute').value;
    if (attribute_value === "") {
        attribute_error.style.display = "block";
        attribute_input.style.borderColor = "red";
        isValid = false;
    } else {
        attribute_error.style.display = "none";
        attribute_input.style.borderColor = "#ccc";
    }

    // 説明の検証（空白でないこと）
    if (description === "") {
        description_error.style.display = "block";
        description_input.style.borderColor = "red";
        isValid = false;
    } else {
        description_error.style.display = "none";
        description_input.style.borderColor = "#ccc";
    }
    return isValid;
}