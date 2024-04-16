// Cargar los datos
d3.json("../data.json").then(function(data) {

    // Crear un objeto de recuento de Pokémon por versión de juego
    var pokemonCounts = {};
    
    // Inicializar el contador para cada versión de juego
    data.versiones_de_juego.forEach(function(version) {
        pokemonCounts[version] = 0;
    });

    // Contar los Pokémon por versión de juego
    data.pokemon_nombres.forEach(function(pokemonName) {
        // Incrementar el contador para cada versión en la que aparece el Pokémon
        data.versiones_de_juego.forEach(function(version) {
            if (data.versiones_de_juego.includes(version)) {
                pokemonCounts[version]++;
            }
        });
    });

    // Convertir el objeto en un array de objetos {version: ..., count: ...}
    var pieData = Object.keys(pokemonCounts).map(function(version) {
        return { version: version, count: pokemonCounts[version] };
    });

    // Crear el generador de arcos para el gráfico de pastel
    var arcGenerator = d3.arc()
        .innerRadius(0)
        .outerRadius(150);

    // Crear el generador de colores
    var color = d3.scaleOrdinal()
        .domain(pieData.map(d => d.version))
        .range(d3.schemeCategory10);

    // Crear el generador de pie
    var pieGenerator = d3.pie()
        .value(d => d.count);

    // Seleccionar el contenedor del gráfico
    var chart = d3.select("#chart");

    // Añadir los arcos al gráfico
    chart.selectAll(".arc")
        .data(pieGenerator(pieData))
        .enter().append("path")
        .attr("class", "arc")
        .attr("d", arcGenerator)
        .attr("fill", d => color(d.data.version))
        .attr("transform", "translate(200,200)");
}).catch(function(error) {
    // Manejar cualquier error de carga
    console.error('Error al cargar el archivo JSON:', error);
});
