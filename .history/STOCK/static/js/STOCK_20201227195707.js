function doSomethingWithData(error, jsondata) {

    const object = JSON.parse(jsondata)
    object.forEach(function(obj) {
        var jsonObj = [];

        jsonObj.push(obj.fields);
    });




}
/*
const loadData = d3.json('/Chart_data/06N', (error, jsondata) => {

    const object = JSON.parse(jsondata)

    return object.map((item) => ({

        date: new Date(item.fields.Day_trading * 1000),
        high: item.fields.Highest_price,
        low: item.fields.Lowest_price,
        open: item.fields.Opening_price,
        close: item.fields.Closing_price,
        volume: item.fields.Volume,
    }))

});
*/
const months = { 0: 'sty', 1: 'lut', 2: 'mar', 3: 'kwi', 4: 'may', 5: 'cze', 6: 'lip', 7: 'sie', 8: 'wrz', 9: 'paź', 10: 'lis', 11: 'gru' }

function sortdata(json) {

    return json.map((item) => ({

        date: new Date(item.fields.Day_trading),
        high: item.fields.Highest_price,
        low: item.fields.Lowest_price,
        open: item.fields.Opening_price,
        close: item.fields.Closing_price,
        volume: item.fields.Volume,

    }))
}



var sort_Data = sortdata(data)
const date_D = sort_Data.slice(-240)


const date_M = () => {
        arr = [];
        sort_Data.map((item) => {
            var monthinYear = item.date.getMonth() + '-' + item.date.getFullYear()

            if (arr.find(obj => {
                    return obj.date === monthinYear
                })) {

                arr.find(obj => {
                    return obj.date === monthinYear
                }).add = [item.high, item.close, item.low, item.open, item.volume]

            } else {
                arr.push({
                    'date': monthinYear,
                    'fields': {
                        'high': [item.high],
                        'close': [item.close],
                        'low': [item.low],
                        'open': [item.open],
                        'volume': [item.volume],
                    },
                    set add(value) {

                        this.fields.high.push(value[0])
                        this.fields.close.push(value[1])
                        this.fields.low.push(value[2])
                        this.fields.open.push(value[3])
                        this.fields.volume.push(value[4])
                    }
                })

            }



        })
        return arr.map((item) => ({

            date: new Date('01-' + item.date),
            high: Math.max.apply(null, item.fields.high),
            low: Math.min.apply(null, item.fields.low),
            open: item.fields.open[0],
            close: item.fields.close[-1],
            volume: item.fields.volume.reduce((a, b) => {
                return a + b;
            }),

        }))
    }
    /*
    var month_date = date_M()
    console.log(month_date)
    */



var chart = d3.select("#chart")
    .append("svg:svg")
    .attr("class", "chart")


var points = []



function chart_zoom(range_data, selection) {
    console.log(selection)
    var zoom_off = false

    var t
    var xScaleZ

    var margin = { top: 40, right: 30, bottom: 30, left: 30 },
        width = 1080,
        height = 500 - margin.top - margin.bottom;
    if (range_data[0] <= 0) {
        range_data = [0, range_data[1]]
    } else if (range_data[1] >= sort_Data.length) {
        range_data = [range_data[0], sort_Data.length - 1]
    } else if (range_data[0] <= 0 && range_data[1] >= sort_Data.length) {
        range_data = [0, sort_Data.length - 1]
    }

    filtered_data = _.filter(sort_Data, d => ((d.date >= sort_Data[range_data[0]].date) && (d.date <= sort_Data[range_data[1]].date)))
    console.log(filtered_data.length)
    var xScale = d3.scaleLinear().domain([-1, filtered_data.length])
        .range([0, width])
    var xBand = d3.scaleBand().domain(d3.range(-1, filtered_data.length)).range([0, width]).padding(0.3)

    var xDateScale = d3.scaleQuantize().domain([0, filtered_data.length]).range(filtered_data)
    const Rick_date_value = (date) => {
        var date_axis = []
        date.map((x, i, arr) => {

            d = x.date
            v = arr[i - 1]
            if (i === 0) {
                date_axis.push(i)
            } else {
                if (d.getMonth() !== v.date.getMonth() && d.getFullYear() === v.date.getFullYear()) {
                    date_axis.push(i)
                }
                if (d.getMonth() !== v.date.getMonth() && d.getFullYear() !== v.date.getFullYear()) {

                    date_axis.push(i)
                }
            }

        })

        return date_axis
    }

    var xAxis = d3.axisBottom()
        .scale(xScale)
        .tickValues(Rick_date_value(filtered_data))
        .tickFormat((x, i, arr) => {
            d = filtered_data[x]
            v = filtered_data[x - 1]
            if (i === 0) {
                date_axis = d.date.getFullYear()
                return date_axis
            } else {
                if (d.date.getMonth() !== v.date.getMonth() && d.date.getFullYear() === v.date.getFullYear()) {
                    date_axis = months[d.date.getMonth()]
                    return date_axis
                }
                if (d.date.getMonth() !== v.date.getMonth() && d.date.getFullYear() !== v.date.getFullYear()) {

                    date_axis = d.date.getFullYear()
                    return date_axis
                }
            }

        })
        .tickSizeInner([-height])

    var ymin = d3.min(filtered_data.map((x) => { return x.low; }));
    var ymax = d3.max(filtered_data.map((x) => { return x.high; }));
    var yScale = d3.scaleLinear().domain([ymin, ymax]).range([height, 0]).nice();
    var yAxis = d3.axisRight()
        .scale(yScale)
        .tickSize(width)

    chart
        .attr("viewBox", [0, 0, width, height + margin.top + margin.bottom])
        .append("g")
        .attr("id", "g_chart")
        .attr("transform", "translate(" + 0 + "," + margin.top + ")");

    chart
        .append("rect")
        .attr("id", "rect")
        .attr("width", width)
        .attr("height", height)
        .style("fill", "#E5E5E5")
        .style("pointer-events", "all")
        .attr("clip-path", "url(#clip)")

    var gX = chart.append("g")
        .attr("class", "axis x-axis") //Assign "axis" class
        .attr("transform", "translate(0," + height + ")")
        .style("fill", "#E5E5E5")
        .call(xAxis)
        .call(g => g.selectAll(".tick line")
            .attr("stroke-opacity", 0.5)
            .attr("stroke-dasharray", "2,2"))
        .call(g => g.select(".domain")
            .remove())

    var gY = chart.append("g")
        .attr("class", "axis y-axis")
        .attr("transform", `translate(0,0)`)
        .style("fill", "#E5E5E5")
        .call(yAxis)
        .call(g => g.select(".domain")
            .remove())
        .call(g => g.selectAll(".tick line")
            .attr("stroke-opacity", 0.5)
            .attr("stroke-dasharray", "2,2"))
        .call(g => g.selectAll(".tick text")
            .attr("x", 40)
            .attr("dy", -4))

    var chartBody = chart.append("g")
        .attr("class", "chartBody")
        .attr("clip-path", "url(#clip)");


    let candles = chartBody.selectAll(".candle")
        .data(filtered_data)
        .enter()
        .append("rect")
        .attr('x', (data, i) => xScale(i) - xBand.bandwidth())
        .attr("class", "candle")
        .attr('y', data => yScale(Math.max(data.open, data.close)))
        .attr('width', xBand.bandwidth())
        .attr('height', d => (d.open === d.close) ? 1 : yScale(Math.min(d.open, d.close)) - yScale(Math.max(d.open, d.close)))
        .attr("fill", d => (d.open === d.close) ? "silver" : (d.open > d.close) ? "red" : "green")
        .style("stroke", 'black')
        .style("stroke-width", 0.5);

    let stems = chartBody.selectAll("g.line")
        .data(filtered_data)
        .enter()
        .append("line")
        .attr("class", "stem")
        .attr("x1", (d, i) => xScale(i) - xBand.bandwidth() / 2)
        .attr("x2", (d, i) => xScale(i) - xBand.bandwidth() / 2)
        .attr("y1", d => yScale(d.high))
        .attr("y2", d => yScale(d.low))
        .attr("stroke", d => (d.open === d.close) ? "black" : (d.open > d.close) ? "red" : "green")

    const extent = [
        [margin.left, 0],
        [width - margin.right, height]
    ];

    var resizeTimer;
    var zoom = d3.zoom()
        .scaleExtent([1, 5])
        .translateExtent(extent)
        .extent(extent)
        .on("zoom", zoomed)
        .on('zoom.end', zoomend);


    chart.call(zoom)



    var button = d3.select("#chart")
        .append("button")
        .attr('width', 20)
        .attr('height', 20)
        .attr("type", "button")
        .attr("class", "btn-btn")
        .text("linia")
        .style("position", "absolute")
        .style("left", "85%")
        .style("top", "50px")
        .on('click', createDot)


    let drag = d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended);

    let moveLine = d3.drag()
        .subject(function() {
            var t = d3.select(this);

            return { x1: t.attr("x1"), y1: t.attr("y1"), x2: t.attr("x2"), y2: t.attr("y2") };
        })
        .on("start", dragstarted)
        .on('drag', dragLine)
        .on('end', dragended);
    var drag_start = []

    function dragstarted() {
        zoom_off = true
        var x = d3.event.x;
        var y = d3.event.y;
        drag_start.push(x, y)

    }


    function dragged() {
        var cx = d3.event.x;
        var cy = d3.event.y;
        d3.select(this)
            .attr('cx', cx)
            .attr('cy', cy)

        var linia_drag = d3.select(`#${ this.id.substr(0, 5)} `)

        if (this.className.baseVal === 'start') {
            console.log("if")
            linia_drag
                .attr('x1', cx)
                .attr('y1', cy)

            var arrpoints = points.find(x => x.name === this.id.substr(0, 5))
            arrpoints.xy[0] = cx
            arrpoints.xy[1] = cy
        } else {
            linia_drag
                .attr('x2', cx)
                .attr('y2', cy)
            var arrpoints = points.find(x => x.name === this.id.substr(0, 5))
            arrpoints.xy[2] = cx
            arrpoints.xy[3] = cy
        }
    }

    function dragLine() {
        var x = d3.event.x;
        var y = d3.event.y;

        var Nx = drag_start[0] - x
        var Ny = drag_start[1] - y

        var line_drag = d3.select(this);

        var attributes = {
            "x1": d3.event.subject.x1 - Nx,
            "y1": d3.event.subject.y1 - Ny,

            "x2": d3.event.subject.x2 - Nx,
            "y2": d3.event.subject.y2 - Ny,
        };

        line_drag
            .attr("x1", attributes.x1)
            .attr("y1", attributes.y1)
            .attr("x2", attributes.x2)
            .attr("y2", attributes.y2)
        var circle_start = d3.select(`#${this.id}Start`)
        circle_start
            .attr("cx", attributes.x1)
            .attr("cy", attributes.y1)
        var circle_end = d3.select(`#${this.id}End`)
        circle_end
            .attr("cx", attributes.x2)
            .attr("cy", attributes.y2)

    }

    function dragended() {
        zoom_off = false
        drag_start = []
    }

    var div = d3.select("#rect");

    var line1;
    var circles1;
    var circles2;

    function createDot() {



        zoom_off = true
        var name = "Line" + (points.length + 1)

        isDrawing = true;
        vardata_circle = []
        scale_var = []

        div.on("click", function() {

            var m = d3.mouse(this);

            vardata_circle.push(m[0], m[1])
            if (xScaleZ) {
                console.log(xScaleZ.invert(m[0]))
                scale_var.push(xScaleZ.invert(m[0]), yScale.invert(m[1]))
            } else {
                scale_var.push(xScale.invert(m[0]), yScale.invert(m[1]))
            }
            line = chart.append("g")
                .attr("class", "tradingLIne")
            line1 = line.append("line")
                .attr("id", `${ name }`)
                .attr("class", "drowLine")
                .attr("x1", m[0])
                .attr("y1", m[1])
                .attr("x2", m[0])
                .attr("y2", m[1])
                .attr("stroke-width", 1)
                .attr("stroke", "black")




            div.on("mousemove", () => {
                if (isDrawing === true) {
                    var m = d3.mouse(this);
                    line1.attr("x2", m[0])
                        .attr("y2", m[1]);
                    chart.on("click", function() {
                        div.on("mousemove", null)
                        div.on("click", null);
                        chart.on("click", null);
                        vardata_circle.push(m[0], m[1])
                        if (xScaleZ) {
                            console.log(xScaleZ.invert(m[0]))
                            scale_var.push(xScaleZ.invert(m[0]), yScale.invert(m[1]))
                        } else {
                            scale_var.push(xScale.invert(m[0]), yScale.invert(m[1]))
                        }
                        points.push({
                            "name": name,
                            "xy": vardata_circle,
                            "scale": scale_var

                        })
                        isDrawing = false;
                        circles1 = line.append('circle')
                            .attr("id", `${name}Start`)
                            .attr('class', 'start')
                            .attr('r', 2.0)
                            .attr('cx', vardata_circle[0])
                            .attr('cy', vardata_circle[1])
                            .style('cursor', 'pointer')
                            .style('fill', "black");
                        circles2 = line.append('circle')
                            .attr("id", `${name}End`)
                            .attr('class', 'End')
                            .attr('r', 2.0)
                            .attr('cx', vardata_circle[2])
                            .attr('cy', vardata_circle[3])
                            .style('cursor', 'pointer')
                            .style('fill', "black");
                        zoom_off = false

                        line.selectAll('circle')
                            .call(drag);

                        line1.style('cursor', 'all-scroll')
                            .call(moveLine)

                        console.log(points)
                        console.log(line1)




                    });
                }

            })

        });


    }

    function zoomed() {
        if (zoom_off === false) {
            console.log("zoom")



            t = d3.event.transform;
            console.log(t)
            console.log(t.x)
            console.log(t.y)
            console.log(d3.event)
            xScaleZ = t.rescaleX(xScale);
            console.log(xScaleZ(1))
            var line_zoom = chart.selectAll(".drowLine")
                .attr("x1", (line_zoom, x, arr) => {
                    console.log(points)
                    console.log(arr[x].id)
                    var arrpoints = points.find(i => i.name === arr[x].id)
                    console.log(arrpoints.xy[0])
                    console.log(arrpoints.scale[0])
                    return xScaleZ(arrpoints.scale[0])
                })
                .attr("x2", (line_zoom, x, arr) => {
                    console.log(points)
                    console.log(arr[x].id)
                    var arrpoints = points.find(i => i.name === arr[x].id)
                    console.log(arrpoints.xy[2])
                    console.log(arrpoints.scale[2])
                    return xScaleZ(arrpoints.scale[2])
                })

            gX.call(
                d3.axisBottom(xScaleZ)
                .tickValues(Rick_date_value(filtered_data))
                .tickFormat((x, i, arr) => {

                    d = filtered_data[x]
                    v = filtered_data[x - 1]
                    if (i === 0) {
                        date_axis = d.date.getFullYear()
                        return date_axis
                    } else {
                        if (d.date.getMonth() !== v.date.getMonth() && d.date.getFullYear() === v.date.getFullYear()) {
                            date_axis = months[d.date.getMonth()]
                            return date_axis
                        }
                        if (d.date.getMonth() !== v.date.getMonth() && d.date.getFullYear() !== v.date.getFullYear()) {

                            date_axis = d.date.getFullYear()
                            return date_axis
                        }
                    }

                })
                .tickSizeInner([-height])
            )

            .call(g => g.selectAll(".tick line")
                    .attr("stroke-opacity", 0.5)
                    .attr("stroke-dasharray", "2,2"))
                .style("fill", "#E5E5E5")
                .call(g => g.select(".domain")
                    .remove())


            candles.attr("x", (data, i) => xScaleZ(i) - (xBand.bandwidth() * t.k) / 2)
                .attr("width", xBand.bandwidth() * t.k);
            stems.attr("x1", (data, i) => xScaleZ(i) - xBand.bandwidth() / 2 + xBand.bandwidth() * 0.5);
            stems.attr("x2", (data, i) => xScaleZ(i) - xBand.bandwidth() / 2 + xBand.bandwidth() * 0.5);

        }


    }

    function zoomend() {
        if (zoom_off === false) {
            console.log("zoomend")
            t = d3.event.transform;
            console.log(t)
            let xScaleZ = t.rescaleX(xScale);
            clearTimeout(resizeTimer)

            resizeTimer = setTimeout(function() {

                var xmin = xDateScale(Math.floor(xScaleZ.domain()[0])).date
                xmax = xDateScale(Math.floor(xScaleZ.domain()[1])).date
                filtered = _.filter(filtered_data, d => ((d.date >= xmin) && (d.date <= xmax)))

                minP = +d3.min(filtered, d => d.low)
                maxP = +d3.max(filtered, d => d.high)
                buffer = Math.floor((maxP - minP) * 0.3)

                yScale.domain([minP - buffer, maxP + buffer])
                console.log(yScale)
                candles.transition()
                    .duration(2)
                    .attr("y", (d) => yScale(Math.max(d.open, d.close)))
                    .attr("height", d => (d.open === d.close) ? 1 : yScale(Math.min(d.open, d.close)) - yScale(Math.max(d.open, d.close)));

                stems.transition().duration(2)
                    .attr("y1", (d) => yScale(d.high))
                    .attr("y2", (d) => yScale(d.low))

                gY.transition()
                    .call(d3.axisRight()
                        .scale(yScale)
                        .tickSize(width)
                    )
                    .attr("transform", `translate(0, 0)`)
                    .call(g => g.select(".domain")
                        .remove())
                    .call(g => g.selectAll(".tick:not(:first-of-type) line")
                        .attr("stroke-opacity", 0.5)
                        .attr("stroke-dasharray", "2,2"))
                    .call(g => g.selectAll(".tick text")
                        .attr("x", 40)
                        .attr("y", -4))
                    .style("fill", "#E5E5E5")

                var line_zoom = chart.selectAll(".drowLine")
                    .attr("y1", (line_zoom, x, arr) => {
                        console.log(points)
                        console.log(arr[x].id)
                        var arrpoints = points.find(i => i.name === arr[x].id)
                        console.log(arrpoints.xy[0])
                        console.log(yScale(arrpoints.scale[1]))
                        return yScale(arrpoints.scale[1])
                    })
                    .attr("y2", (line_zoom, x, arr) => {
                        console.log(points)
                        console.log(arr[x].id)
                        var arrpoints = points.find(i => i.name === arr[x].id)
                        console.log(arrpoints.xy[2])
                        console.log(yScale(arrpoints.scale[3]))
                        return yScale(arrpoints.scale[3])
                    })


            }, 500)

        }
    }


}


var width_focus = 1100,
    margin_bottom = 20,
    height_focus = 200 + margin_bottom;


var xScale_focus = d3.scaleLinear().domain([-1, sort_Data.length])
    .range([0, width_focus])
var ymin_focus = d3.min(sort_Data.map((x) => { return x.low; }));
var ymax_focus = d3.max(sort_Data.map((x) => { return x.high; }));
var yScale_focus = d3.scaleLinear().domain([ymin_focus, ymax_focus]).range([height_focus, 0]).nice();

const FullYear_date_value = (date) => {
    var date_axis = []
    date.map((x, i, arr) => {
        d = x.date
        v = arr[i - 1]
        if (i === 0) {
            date_axis.push(i)
        } else {
            if (d.getMonth() !== v.date.getMonth() && d.getFullYear() !== v.date.getFullYear()) {
                date_axis.push(i)
            }
        }
    })

    return date_axis
}
var xAxis_focus = d3.axisBottom()
    .scale(xScale_focus)
    .tickValues(FullYear_date_value(sort_Data))
    .tickFormat((x, i, arr) => {
        d = sort_Data[x]
        v = sort_Data[x - 1]
        if (i === 0) {
            date_axis = d.date.getFullYear()
            return date_axis
        } else {

            if (d.date.getMonth() !== v.date.getMonth() && d.date.getFullYear() !== v.date.getFullYear()) {

                date_axis = d.date.getFullYear()
                return date_axis
            }
        }
    })


var areaGenerator = d3.area()
    .x((d, i) => { return xScale_focus(i) })
    .y0(yScale_focus(0))
    .y1(function(d) { return yScale_focus(d.high) })
var focus_chart = d3.select("#chart")
    .append("svg:svg")
    .attr("viewBox", [0, 0, width_focus, height_focus + margin_bottom])

focus_chart
    .append("g")
    .attr("id", "g_chart_focus")
    .attr("transform", "translate(" + 0 + "," + 20 + ")");

var gX_focus = focus_chart.append("g")
    .attr("class", "axis x-axis_focus") //Assign "axis" class
    .attr("transform", `translate(0,${height_focus})`)
    .style("fill", "#E5E5E5")
    .call(xAxis_focus)



var area = focus_chart.append('g')
    .attr("clip-path", "url(#clip)")

var brush = d3.brushX() // Add the brush feature using the d3.brush function
    .extent([
        [0, 0],
        [width_focus, height_focus]
    ]) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
    .on("brush", brushed)
    .on("end", brushended);

area.append("path")
    .datum(sort_Data)
    .attr("class", "myArea") // I add the class myArea to be able to modify it later on.
    .attr("fill", "#69b3a2")
    .attr("fill-opacity", .3)
    .attr("stroke", "black")
    .attr("stroke-width", 1)
    .attr("d", areaGenerator)

const defaultSelection = [0, 100]

area
    .append("g")
    .attr("class", "brush")
    .call(brush)
    .call(brush.move, defaultSelection);

function brushed() {

    const selection = d3.event.selection;

    if (selection) {
        console.log("selection")

    }
}


function brushended() {

    const selection = d3.event.selection;

    if (!selection) {
        area.call(brush.move, defaultSelection);

    } else {
        range_data = [Math.floor(xScale_focus.invert(selection[0])), Math.floor(xScale_focus.invert(selection[1]))]
        chart.selectAll("*").remove();
        chart_zoom(range_data, selection)

    }
}












scroll_element = document.getElementById("g_chart")
var down = false;
var scrollLeft = 0
var scroll_x = 0
scroll_element.addEventListener('mousedown', e => {
    if (scroll) {

        scroll_element_move = document.getElementById("chart")

        down = true;
        scrollLeft = scroll_element_move.scrollLeft;
        scroll_x = e.clientX;
        scroll_element.addEventListener('mouseup', () => {
            down = false;
        })
        scroll_element.addEventListener('mousemove', e => {

            if (down) {
                scroll_value = scrollLeft + scroll_x - e.clientX
                if (scroll_value >= 4) {
                    gY.selectAll(".tick text").attr('x', scrollLeft + scroll_x - e.clientX)
                }

                scroll_element_move.scrollLeft = scroll_value;
            }

        })
        scroll_element.addEventListener('mouseleave', () => {
            down = false;
        })

    }

})