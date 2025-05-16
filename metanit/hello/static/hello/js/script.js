document.addEventListener('DOMContentLoaded', function() {
    const budgetSlider = document.getElementById('budget');
    const budgetValue = document.getElementById('budget-value');
    const generateBtn = document.getElementById('generate-btn');
    const resultsDiv = document.getElementById('results');
    
    // Форматирование числа с пробелами
    function formatNumber(num) {
        return new Intl.NumberFormat('ru-RU').format(num);
    }
    
    // Обновление отображаемого значения бюджета
    budgetSlider.addEventListener('input', function() {
        budgetValue.textContent = formatNumber(this.value) + ' руб';
    });
    
    // Обработка нажатия кнопки
    generateBtn.addEventListener('click', function() {
        const budget = budgetSlider.value;
        const purpose = document.getElementById('purpose').value;
        const priority = document.getElementById('priority').value;
        
        // Показываем загрузку
        resultsDiv.innerHTML = `
            <div class="loading">
                <h2>Подбираем лучшие варианты...</h2>
                <p>Пожалуйста, подождите</p>
                <div class="loader"></div>
            </div>
        `;
        resultsDiv.style.display = 'block';
        
        // Запрос к API
        fetch(`/api/builds?budget=${budget}&purpose=${purpose}&priority=${priority}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка сети');
                }
                return response.json();
            })
            .then(data => displayBuilds(data))
            .catch(error => {
                console.error('Ошибка:', error);
                resultsDiv.innerHTML = `
                    <div class="error">
                        <h2>Произошла ошибка</h2>
                        <p>${error.message}</p>
                        <button onclick="window.location.reload()">Обновить страницу</button>
                    </div>
                `;
            });
    });
    
    // Отображение результатов
    function displayBuilds(builds) {
        if (!builds || builds.length === 0) {
            resultsDiv.innerHTML = `
                <div class="no-results">
                    <h2>Не найдено подходящих сборок</h2>
                    <p>Попробуйте изменить параметры поиска или увеличить бюджет.</p>
                </div>
            `;
            return;
        }
        
        let html = '<h2>Подходящие сборки</h2>';
        
        builds.forEach(build => {
            html += `
                <div class="build-card">
                    <h3>${build.name} - ${formatNumber(build.totalPrice)} руб</h3>
                    <ul>
                        ${build.components.map(comp => 
                            `<li>${comp.name} - ${formatNumber(comp.price)} руб</li>`
                        ).join('')}
                    </ul>
                    <button class="select-build" data-id="${build.id}">Выбрать эту сборку</button>
                </div>
            `;
        });
        
        resultsDiv.innerHTML = html;
        
        // Добавляем обработчики для кнопок выбора
        document.querySelectorAll('.select-build').forEach(button => {
            button.addEventListener('click', function() {
                const buildId = this.getAttribute('data-id');
                alert(`Выбрана сборка #${buildId}. В реальном приложении здесь будет переход к оформлению.`);
            });
        });
    }
});