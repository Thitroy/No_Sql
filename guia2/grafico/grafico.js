// Cargar los datos
document.addEventListener("DOMContentLoaded", function() {
d3.json("../data.json").then(function(data) {
    console.log(data);

    // Filtrar los datos para obtener solo los de Kanto y Johto
    var kantoData = data.regiones.find(region => region.nombre === "Kanto");
    var johtoData = data.regiones.find(region => region.nombre === "Johto");

    // Obtener la cantidad de juegos que incluyen cada región
    var kantoGamesCount = kantoData.juegos_donde_se_incluye.length;
    var johtoGamesCount = johtoData.juegos_donde_se_incluye.length;

    console.log(kantoGamesCount);
    console.log(johtoGamesCount);

    // Crear los datos para el gráfico de barras de juegos
    var gamesBarData = [
        { region: "Kanto", count: kantoGamesCount },
        { region: "Johto", count: johtoGamesCount }
    ];

    // Crear el generador de barra para juegos
    var gamesBarGenerator = d3.scaleBand()
        .range([0, 400])
        .padding(0.1);

        console.log(gamesBarGenerator);

    // Seleccionar el contenedor del gráfico de juegos
    var gamesChart = d3.select("#games-chart");

    // Configurar el dominio para el generador de barra de juegos
    gamesBarGenerator.domain(gamesBarData.map(d => d.region));

    // Añadir las barras al gráfico de juegos
    gamesChart.selectAll(".games-bar")
        .data(gamesBarData)
        .enter().append("rect")
        .attr("class", "games-bar")
        .attr("x", d => gamesBarGenerator(d.region))
        .attr("y", d => 200 - (d.count * 10))
        .attr("width", gamesBarGenerator.bandwidth())
        .attr("height", d => d.count * 10)
        .attr("fill", d => d.region === "Kanto" ? "blue" : "green");

        console.log(gamesChart);

    // Añadir un título al gráfico de barras de juegos
    gamesChart.append("text")
        .attr("x", 200)
        .attr("y", 30)
        .attr("text-anchor", "middle")
        .attr("font-size", "20px")
        .text("Comparación de juegos entre Kanto y Johto");

    // Obtener la cantidad de Pokémon que habitan en cada región
    var kantoPokemonCount = kantoData.pokemons_que_habitan.length;
    var johtoPokemonCount = johtoData.pokemons_que_habitan.length;

    // Crear los datos para el gráfico de pastel de Pokémon
    var pokemonPieData = [
        { region: "Kanto", count: kantoPokemonCount },
        { region: "Johto", count: johtoPokemonCount }
    ];

    // Crear el generador de arcos para el gráfico de pastel de Pokémon
    var pokemonArcGenerator = d3.arc()
        .innerRadius(0)
        .outerRadius(150);

    // Seleccionar el contenedor del gráfico de pastel de Pokémon
    var pokemonChart = d3.select("#pokemon-chart");

    // Crear el generador de colores
    var color = d3.scaleOrdinal()
        .domain(pokemonPieData.map(d => d.region))
        .range(["blue", "green"]); // Colores correspondientes a Kanto y Johto

    // Crear el generador de pie
    var pokemonPieGenerator = d3.pie()
        .value(d => d.count);

    // Añadir los arcos al gráfico de pastel de Pokémon
    pokemonChart.selectAll(".pokemon-arc")
        .data(pokemonPieGenerator(pokemonPieData))
        .enter().append("path")
        .attr("class", "pokemon-arc")
        .attr("d", pokemonArcGenerator)
        .attr("fill", d => color(d.data.region))
        .attr("transform", "translate(200,200)");
        
   // Añadir un título al gráfico de pastel de Pokémon
   pokemonChart.append("text")
   .attr("x", 200)
   .attr("y", 30)
   .attr("text-anchor", "middle")
   .attr("font-size", "20px")
   .text("Comparación de Pokémon entre Kanto y Johto");
  
});
});
