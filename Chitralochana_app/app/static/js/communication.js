$(document).ready( function(){
    namespace = '/analyze';
    var socket = io.connect('http://'+document.domain+':'+location.port+namespace);

    socket.on('connect', function(){
        socket.emit('response event', {reply: 'I am connected!'});
    });

    socket.on('stats', function(data){
        //alert('recieved message');

        stats = JSON.parse(data)
        console.debug(stats)
        $('#tweets-nos span').text(stats.TotalTweets.toString());
        $('#user-nos span').text(stats.TotalUsers.toString());
        $('#hashtag-searchs').text(stats.Hashtags)

        top5tags = stats.Top5Hashtags

        var width = 1000;
        var barHeight = 20;
        var totalheight = 150;


        $('.barchart').empty();

        var x = d3.scale.linear()
                    .domain([0, d3.max(top5tags, function(d){
                        return d[1];
                    })])
                    .range([0, width]);

        var y = d3.scale.ordinal()
                    .domain(top5tags)
                    .rangeBands([0, totalheight]);

        var barchart = d3.select(".barchart")
                        .append("svg:svg")
                        .attr("width", width)
                        .attr("height", y);

        var bar = barchart.selectAll("g")
                        .data(top5tags)
                        .enter().append("g")
                        .attr("transform", function(d, i) { return "translate(0,15)"; });

        bar.append("rect")
            .attr("width", function(d){
                return x(d[1]);
            })
            .attr("y", y)
            .attr("height", y.rangeBand());

        bar.append("text")
            .attr("x", function(d) { return x(d[1]); })
            .attr("y", function(d) { return y(d) + y.rangeBand() / 2; })
            .attr("dy", ".35em")
            .text(function(d) { return d[0]+':'+d[1]; });

        barchart.selectAll("line")
            .data(x.ticks(10))
            .enter().append("svg:line")
            .attr("x1", function(d){
                return x(d[1]);
            })
            .attr("x2", function(d){
                return x(d[1]);
            })
            .attr("y1", 0)
            .attr("y2", totalheight)
            .attr("stroke", "#ccc");

            barchart.selectAll("text.rule")
                    .data(x.ticks(10))
                    .enter().append("svg:text")
                    .attr("class", "rule")
                    .attr("x", function(d){
                        return x(d[1]);
                    })
                    .attr("y", 0)
                    .attr("dy", -3)
                    .attr("text-anchor", "middle")
                    .text(String);

        barchart.append("svg:line")
            .attr("y1", 0)
            .attr("y2", totalheight)
            .attr("stroke", "#000");

        /*d3.select(".barchart")
            .selectAll("div")
            .data(top5tags)
            .enter().append("div")
            .style("width", function(d) { return x(d[1])  + "px"; })
            .text(function(d) { return d[0]; });*/
    });

})