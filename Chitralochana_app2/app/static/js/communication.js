$(document).ready( function(){
    namespace = '/analyze';
    var socket = io.connect('http://'+document.domain+':'+location.port+namespace, {'connect timeout': 1000});

    socket.on('connect', function(){
        socket.emit('response event', {reply: 'I am connected!'});
    });

    socket.on('stats', function(data){

        stats = JSON.parse(data)
        console.debug(stats)
        $('#tweets-nos span').text(stats.TotalTweets.toString());
        $('#user-nos span').text(stats.TotalUsers.toString());
        $('#hashtag-searchs').text(stats.Hashtags)

        $('.barchart').empty();
        top5tags = stats.Top5Hashtags;

        var margin = {top: 20, right: 20, bottom: 30, left: 40};
        var width = $(".barchart").width() - margin.left - margin.right;
        var height = 400 - margin.top - margin.bottom;
        var padding = 1;
        // var compareFactors = ["Tweets", "Likes", "Retweets"];

        //var x0 = d3.scale.ordinal()
        //            .rangeRoundBands([0, width], .1)
        //            .domain(top5tags.map(function(d){
        //                return d[0];
        //            }));

        var x_bar = d3.scale.ordinal()
                .rangeRoundBands([0, width], 0.2)
                .domain(top5tags.map(function(d){
                    return d[0];
                }))

        //var x1 = d3.scale.ordinal()
        //            .domain(compareFactors)
        //            .rangeRoundBands([0, x0.rangeBand()]);

        //var color = d3.scale.ordinal()
        //            .range(["#98abc5", "#8a89a6", "#7b6888"]);

        //var colorvalues = ["#98abc5", "#8a89a6", "#7b6888"];

        //var yScale = d3.scale.linear()
        //             .domain([0, d3.max(top5tags, function(d){
        //                return d3.max(d[1], function(d){
        //                    return d;
        //                });
        //             }) ])
        //             .range([0, height]);

        var y_bar = d3.scale.linear()
                    .range([0, height])
                    .domain([0, d3.max(top5tags, function(d){
                        return d[1];
                    })]);

        //var xAxis = d3.svg.axis()
        //            .scale(x0)
        //            .orient("bottom");

        var xAxis_bar = d3.svg.axis()
                        .scale(x_bar)
                        .orient("bottom")

        //var yAxis = d3.svg.axis()
        //            .scale(yScale)
        //            .orient("left")
        //            .tickFormat(d3.format(".2s"));

        var yAxis_bar = d3.svg.axis()
                        .scale(y_bar)
                        .orient("left")
                        .ticks(2);

        var barchart = d3.select(".barchart")
                        .append("svg:svg")
                        .attr("width", width + margin.left + margin.right)
                        .attr("height", height + margin.top + margin.bottom)
                        .append("g")
                        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


        //barchart.append("g")
        //        .attr("class", "x axis")
        //        .attr("transform", "translate(0," + height+")")
        //        .call(xAxis);

        barchart.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height+")")
                .call(xAxis_bar)

        //barchart.append("g")
        //        .attr("class", "y axis")
        //        .call(yAxis);

        barchart.append("g")
                .attr("class", "y axis")
                .call(yAxis_bar)

        //var grpHtag = barchart.selectAll(".tophashtags")
        //                        .data(top5tags)
        //                        .enter()
        //                        .append("g")
        //                        .attr("class", "tophashtags")
        //                        .attr("transform", function(d){
        //                            return "translate("+x0(d[0])+",0)";
        //                        });

        var barHtag = barchart.selectAll(".tophashtags")
                              .data(top5tags)
                              .enter()

        barHtag.append("rect")
                .style("fill", "steelblue")
                .attr("x", function(d){
                    return x_bar(d[0]);
                })
                .attr("width", x_bar.rangeBand())
                .attr("y", function(d){
                    return height - y_bar(d[1]);
                })
                .attr("height", function(d){
                    return y_bar(d[1]);
                });


        //grpHtag.selectAll("rect")
        //        .data(function(d){
        //            return d[1];
        //        })
        //        .enter()
        //        .append("rect")
        //        .attr("width", x1.rangeBand())
        //        .attr("x", function(d,i){
        //            return x1(compareFactors[i]);
        //        })
        //        .attr("y", function(d){
        //            return height - yScale(d);
        //        })
        //        .attr("height", function(d){
        //            return yScale(d);
        //        })
        //        .style("fill", function(d,i){
        //            return colorvalues[i];
        //        });

        //var legend = barchart.selectAll(".legend")
        //    .data(compareFactors)
        //    .enter().append("g")
        //    .attr("class", "legend")
        //    .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

        //legend.append("rect")
        //    .attr("x", width - 18)
        //    .attr("width", 18)
        //    .attr("height", 18)
        //    .style("fill", function(d, i){
        //        return colorvalues[i];
        //    });

        //legend.append("text")
        //    .attr("x", width - 24)
        //    .attr("y", 9)
        //    .attr("dy", ".35em")
        //    .style("text-anchor", "end")
        //    .text(function(d, i) { return compareFactors[i]; });

        $('.wordcloudrep').empty();
        wordList = stats.WordList;

        var width_wordlist = $(".wordcloudrep").width();
        var height_wordlist = 400;

        var textScale = d3.scale.linear()
                     .domain([0, d3.max(wordList, function(d){
                        return d[1];
                     }) ])
                     .range([10, 100]);

        var fill_wordList = d3.scale.category20();

        d3.layout.cloud()
                        .size([width_wordlist, height_wordlist])
                        .words(wordList)
                        .padding(1)
                        .rotate(
                            function(){
                                //return ~~(Math.random()*2)*90;
                                return 0;
                            }
                        )
                        .font("Impact")
                        .fontSize(function(d){
                            return textScale(d[1]);
                        })
                        .on("end", draw)
                        .start();

        function draw(wordList)
        {
            d3.select(".wordcloudrep")
            .append("svg")
            .attr("width", width_wordlist)
            .attr("height", height_wordlist)
            .append("g")
            .attr("transform", "translate(" + width_wordlist/2 + "," + height_wordlist/2 + ")")
            .selectAll("text")
            .data(wordList)
            .enter()
            .append("text")
            .style("font-size", function(d){
                return textScale(d[1]) + "px";
            })
            .style("font-family", "Impact")
            .style("fill", function(d, i){
                return fill_wordList(i);
            })
            .style("opacity", 1e-6)
            .attr("text-anchor", "middle")
            .attr("transform", function(d){
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .transition()
            .duration(1000)
            .style("opacity", 1)
            .text(function(d){
                return d[0];
            })

        }

        var pie_pos_color = "#00ff00";
        var pie_neg_color = "#ff0000";

        var pie_colors = [pie_pos_color, pie_neg_color];
        var pie_lab_name = ["positive", "negative"];

        $('.posNegRep').empty();
        posorneg = stats.positiveOrNegative;

        var sen_height = height;
        var sen_width = width;
        var sen_radius = Math.min(sen_width, sen_height)/2;

        var sen_svg = d3.select('.posNegRep')
                        .append('svg')
                        .attr('width', sen_width)
                        .attr('height', sen_height)
                        .append('g')
                        .attr('transform', 'translate('+ (sen_width/2) + ','+(sen_height/2)+')');

        var sen_arc = d3.svg.arc()
                        .innerRadius(0)
                        .outerRadius(sen_radius - 10)

        var sen_lab_arc = d3.svg.arc()
                            .outerRadius(sen_radius - 10)
                            .innerRadius(sen_radius - 10);


        var sen_pie = d3.layout.pie()
                        .value(function(d, i){
                            return d;
                        })
                        .sort(null);

        var sen_g = sen_svg.selectAll('path')
                .data(sen_pie(posorneg))
                .enter()

                sen_g.append('path')
                .attr('d', sen_arc)
                .attr('fill', function(d, i){
                    return pie_colors[i];
                });

        sen_g.append("text")
                .attr("transform", function(d){
                    return "translate(" + sen_lab_arc.centroid(d) + ")";
                })
                .attr("dy", ".35em")
                .text(function(d, i){
                    return pie_lab_name[i];
                })


    });

})