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
var margin = { top: 40, right: 30, bottom: 20, left: 30 },
    width = 1080,
    height = 500 - margin.top - margin.bottom;

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

var Volume_box = d3.select("#chart")
    .append("svg:svg")




var points = []
var pointsH = []



function chart_zoom(range_data, selection) {

    var zoom_off = false
    var t
    var xScaleZ

    if (range_data[0] <= 0) {
        range_data = [0, range_data[1]]
    } else if (range_data[1] >= sort_Data.length) {
        range_data = [range_data[0], sort_Data.length - 1]
    } else if (range_data[0] <= 0 && range_data[1] >= sort_Data.length) {
        range_data = [0, sort_Data.length - 1]
    }

    filtered_data = _.filter(sort_Data, d => ((d.date >= sort_Data[range_data[0]].date) && (d.date <= sort_Data[range_data[1]].date)))

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
    var yScale_volume = d3.scaleLinear().domain([0, d3.max(filtered_data.map((x) => { return x.volume; }))]).range([100, 0]).nice();
    var yAxis = d3.axisRight()
        .scale(yScale)
        .tickSize(width)

    chart
        .attr("viewBox", [0, 0, width, height + margin.bottom])


    chart
        .append("rect")
        .attr("id", "rect")
        .attr("width", width)
        .attr("height", height)
        .style("fill", "#E5E5E5")


    chart.append("defs").append("clipPath")
        .attr("id", "clip")
        .append("rect")
        .attr("width", width)
        .attr("height", height);




    var gX = chart.append("g")
        .attr("class", "axis x-axis") //Assign "axis" class
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .call(g => g.selectAll(".tick line")
            .attr("stroke-opacity", 0.5)
            .attr("stroke-dasharray", "2,2"))
        .call(g => g.select(".domain")
            .remove())
        .style("fill", "#E5E5E5")

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
        .attr("class", "chartBody");



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

    Volume_box.attr("viewBox", [0, 0, width, 100])

    var Volume = Volume_box.selectAll(".volume")
        .data(filtered_data)
        .enter()
        .append("rect")
        .attr('x', (data, i) => xScale(i) - xBand.bandwidth())
        .attr("class", "volume")
        .attr('y', data => yScale_volume(data.volume))
        .attr('width', xBand.bandwidth())
        .attr('height', d => 100 - yScale_volume(d.volume))
        .attr("fill", d => (d.open === d.close) ? "silver" : (d.open > d.close) ? "red" : "green")

    let moveLine = d3.drag()
        .subject(function() {
            var t = d3.select(this);

            return { x1: t.attr("x1"), y1: t.attr("y1"), x2: t.attr("x2"), y2: t.attr("y2") };
        })
        .on("start", dragstarted)
        .on('drag', dragLine)
        .on('end', dragended);

    let moveLineH = d3.drag()
        .subject(function() {
            var t = d3.select(this);

            return { x1: t.attr("x1"), y1: t.attr("y1"), x2: t.attr("x2"), y2: t.attr("y2") };
        })
        .on("start", dragstarted)
        .on('drag', dragLineH)
        .on('end', dragended);

    let drag = d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended);


    points.map((x) => {

        var name = x.name

        if (name.substr(0, 5) === "LineH") {
            var tradingLIne = chart.append("g")
                .attr("class", "HorizontalLIne")
            var line_trend = tradingLIne.append("line")
                .attr("id", `${ x.name }`)
                .attr("class", "drowLine")
                .attr("x1", xScale(x.scale[0]))
                .attr("y1", yScale(x.scale[1]))
                .attr("x2", xScale(x.scale[2]))
                .attr("y2", yScale(x.scale[3]))
                .attr("stroke-width", 1)
                .attr("stroke", "black")
                .style('cursor', 'all-scroll')
                .attr("clip-path", "url(#clip)")
                .call(moveLineH)

        } else {
            var tradingLIne = chart.append("g")
                .attr("class", "tradingLIne")
            var line_trend = tradingLIne.append("line")
                .attr("id", `${ x.name }`)
                .attr("class", "drowLine")
                .attr("x1", xScale((x.scale[0] - xScale_focus.invert(selection[0]))))
                .attr("y1", yScale(x.scale[1]))
                .attr("x2", xScale((x.scale[2] - xScale_focus.invert(selection[0]))))
                .attr("y2", yScale(x.scale[3]))
                .attr("stroke-width", 1)
                .attr("stroke", "black")
                .style('cursor', 'all-scroll')
                .attr("clip-path", "url(#clip)")
                .call(moveLine)

            circles1 = tradingLIne.append('circle')
                .attr("id", `${x.name}Start`)
                .attr('class', 'start')
                .attr('r', 2.0)
                .attr('cx', xScale((x.scale[0] - xScale_focus.invert(selection[0]))))
                .attr('cy', yScale(x.scale[1]))
                .style('cursor', 'pointer')
                .style('fill', "black")
                .call(drag);
            circles2 = tradingLIne.append('circle')
                .attr("id", `${x.name}End`)
                .attr('class', 'End')
                .attr('r', 2.0)
                .attr('cx', xScale((x.scale[2] - xScale_focus.invert(selection[0]))))
                .attr('cy', yScale(x.scale[3]))
                .style('cursor', 'pointer')
                .style('fill', "black")
                .call(drag);
        }
    })


    const extent = [
        [0, 0],
        [width, height]
    ];

    var resizeTimer;
    var zoom = d3.zoom()
        .scaleExtent([1, 5])
        .translateExtent(extent)
        .extent(extent)
        .on("zoom", zoomed)
        .on('zoom.end', zoomend);


    chart.call(zoom)



    var divButton = d3.select("#chart")
        .append("div")
        .style("position", "absolute")
        .style("right", "11%")
        .style("top", "50px")
        .attr("class", "dropdown")
    var lineButton = divButton.append("button")
        .attr("type", "button")
        .attr("class", "btn-btn")
        .text("linia")
        .on('click', drop)
    var content = divButton.append("div")
        .attr("class", "dropdown-content")
        .attr("id", "myDropdow")

    var button_line = content.append("p")
        .attr("type", "button")
        .attr("class", "btn-cont")
        .text("linia")
        .on('click', createDot)
    var button_horizontal = content.append("p")
        .attr("type", "button")
        .attr("class", "btn-cont")
        .text("linia pozioma")
        .on('click', lineHorizontal)


    var timesClicked = 0;

    function drop() {
        timesClicked++;
        console.log("drop")
        if (timesClicked > 1) {
            content.attr("class", "dropdown-content")
            timesClicked = 0
        } else {
            content._groups[0][0].classList.toggle("show");

        }

    }


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
        var arrpoints = points.find(x => x.name === this.id.substr(0, 5))

        if (this.className.baseVal === 'start') {
            console.log("if")
            linia_drag
                .attr('x1', cx)
                .attr('y1', cy)

            if (xScaleZ) {
                arrpoints.scale[0] = xScaleZ.invert(cx) + xScale_focus.invert(selection[0])
                arrpoints.scale[1] = yScale.invert(cy)
            } else {
                arrpoints.scale[0] = xScale.invert(cx) + xScale_focus.invert(selection[0])
                arrpoints.scale[1] = yScale.invert(cy)
            }

        } else {
            linia_drag
                .attr('x2', cx)
                .attr('y2', cy)

            if (xScaleZ) {
                arrpoints.scale[2] = xScaleZ.invert(cx) + xScale_focus.invert(selection[0])
                arrpoints.scale[3] = yScale.invert(cy)
            } else {
                arrpoints.scale[2] = xScale.invert(cx) + xScale_focus.invert(selection[0])
                arrpoints.scale[3] = yScale.invert(cy)
            }
        }
    }

    function dragLineH() {
        var x = d3.event.x;
        var y = d3.event.y;


        var Ny = drag_start[1] - y

        var line_drag = d3.select(this);
        var arrpoints = points.find(x => x.name === this.id.substr(0, 6))
        console.log(arrpoints)

        var attributes = {

            "y1": d3.event.subject.y1 - Ny,
            "y2": d3.event.subject.y2 - Ny,
        };

        line_drag

            .attr("y1", attributes.y1)

        .attr("y2", attributes.y2)

        arrpoints.scale[1] = yScale.invert(attributes.y1)
        arrpoints.scale[3] = yScale.invert(attributes.y2)


    }

    function dragLine() {
        var x = d3.event.x;
        var y = d3.event.y;

        var Nx = drag_start[0] - x
        var Ny = drag_start[1] - y

        var line_drag = d3.select(this);
        var arrpoints = points.find(x => x.name === this.id.substr(0, 5))

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

        if (xScaleZ) {
            arrpoints.scale[0] = xScaleZ.invert(attributes.x1) + xScale_focus.invert(selection[0])
            arrpoints.scale[1] = yScale.invert(attributes.y1)
            arrpoints.scale[2] = xScaleZ.invert(attributes.x2) + xScale_focus.invert(selection[0])
            arrpoints.scale[3] = yScale.invert(attributes.y2)
        } else {
            arrpoints.scale[0] = xScale.invert(attributes.x1) + xScale_focus.invert(selection[0])
            arrpoints.scale[1] = yScale.invert(attributes.y1)
            arrpoints.scale[2] = xScale.invert(attributes.x2) + xScale_focus.invert(selection[0])
            arrpoints.scale[3] = yScale.invert(attributes.y2)
        }

    }

    function dragended() {
        zoom_off = false
        drag_start = []

    }

    var div = d3.select("#rect");



    function lineHorizontal() {
        content.attr("class", "dropdown-content")
        timesClicked = 0
        console.log("line horizontal")
        zoom_off = true
        vardata_circle = []
        scale_var = []

        var length_class = d3.selectAll(".HorizontalLIne")

        var name = "LineH" + (length_class._groups[0].length + 1)
        div.on("click", function() {

            var m = d3.mouse(this);
            console.log(m)
            console.log(xScale(xScale_focus.domain()[1]))
            line = chart.append("g")
                .attr("class", "HorizontalLIne")
            line1 = line.append("line")
                .attr("id", `${name}`)
                .attr("class", "drowLine")
                .attr("x1", xScale(xScale_focus.domain()[0]))
                .attr("y1", m[1])
                .attr("x2", xScale(xScale_focus.domain()[1]))
                .attr("y2", m[1])
                .attr("stroke-width", 1)
                .attr("stroke", "black")
                .attr("clip-path", "url(#clip)")
                .style('cursor', 'all-scroll')
                .call(moveLineH)

            vardata_circle.push(xScale(xScale_focus.domain()[0]), m[1], xScale(xScale_focus.domain()[1]), m[1])
            scale_var.push(xScale_focus.domain()[0], yScale.invert(m[1]), xScale_focus.domain()[1], yScale.invert(m[1]))
            points.push({
                "name": name,
                "xy": vardata_circle,
                "scale": scale_var

            })
            div.on("click", null);
            zoom_off = false

        })
    }

    function createDot() {
        content.attr("class", "dropdown-content")
        timesClicked = 0
        vardata_circle = []
        scale_var = []



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
                scale_var.push(xScaleZ.invert(m[0]) + xScale_focus.invert(selection[0]), yScale.invert(m[1]))
            } else {
                scale_var.push(xScale.invert(m[0]) + xScale_focus.invert(selection[0]), yScale.invert(m[1]))
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
                .attr("clip-path", "url(#clip)")





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
                            scale_var.push(xScaleZ.invert(m[0]) + xScale_focus.invert(selection[0]), yScale.invert(m[1]))
                        } else {
                            scale_var.push(xScale.invert(m[0]) + xScale_focus.invert(selection[0]), yScale.invert(m[1]))
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
            console.log((xScaleZ.domain()))

            var line_zoom = chart.selectAll(".drowLine")
                .attr("x1", (line_zoom, x, arr) => {
                    console.log(points)
                    console.log(arr[x].id)
                    var arrpoints = points.find(i => i.name === arr[x].id)
                    console.log(arrpoints.xy[0])
                    console.log(arrpoints.scale[0])
                    return xScaleZ(arrpoints.scale[0] - xScale_focus.invert(selection[0]))
                })
                .attr("x2", (line_zoom, x, arr) => {
                    console.log(points)
                    console.log(arr[x].id)
                    var arrpoints = points.find(i => i.name === arr[x].id)
                    console.log(arrpoints.xy[2])
                    console.log(arrpoints.scale[2])
                    return xScaleZ(arrpoints.scale[2] - xScale_focus.invert(selection[0]))
                })
            var Circle_zoom = chart.selectAll('circle')
                .attr("cx", (Circle_zoom, x, arr) => {
                    console.log(arr[x])
                    console.log(arr[x].className.baseVal)
                    console.log(points)
                    console.log(arr[x].id.substr(0, 5))
                    var arrpoints = points.find(i => i.name === arr[x].id.substr(0, 5))
                    if (arr[x].className.baseVal === 'start') {
                        console.log("if")
                        console.log(arrpoints.xy[0])
                        console.log(arrpoints.scale[0])
                        return xScaleZ(arrpoints.scale[0] - xScale_focus.invert(selection[0]))

                    } else {
                        console.log("else")
                        console.log(arrpoints.xy[2])
                        console.log(arrpoints.scale[2])
                        return xScaleZ(arrpoints.scale[2] - xScale_focus.invert(selection[0]))
                    }

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

            Volume.attr('x', (data, i) => xScaleZ(i) - xBand.bandwidth())
                .attr('width', xBand.bandwidth() * t.k)

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
                    console.log(xmin)
                    console.log((xScaleZ.domain()))

                    xmax = xDateScale(Math.floor(xScaleZ.domain()[1])).date
                    console.log(xmax)
                    filtered = _.filter(filtered_data, d => ((d.date >= xmin) && (d.date <= xmax)))

                    minP = +d3.min(filtered, d => d.low)
                    maxP = +d3.max(filtered, d => d.high)
                    var buffer = () => {
                        console.log((maxP - minP) * 0.1)
                        if ((maxP - minP) * 0.1 > 1) {
                            console.log("if")
                            return Math.floor((maxP - minP) * 0.1)
                        } else {
                            console.log("else")
                            return Number(((maxP - minP) * 0.1).toFixed(2))
                        }
                    }
                    console.log(minP)
                    console.log(maxP)
                    console.log((maxP - minP) * 0.1)
                    console.log(buffer())
                    yScale.domain([minP - buffer(), maxP + buffer()])
                    console.log(yScale.domain())
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
                        .call(g => g.selectAll(".tick line")
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

                    var Circle_zoom = chart.selectAll('circle')
                        .attr("cy", (Circle_zoom, x, arr) => {
                            console.log(arr[x])
                            console.log(arr[x].className.baseVal)
                            console.log(points)
                            console.log(arr[x].id.substr(0, 5))
                            var arrpoints = points.find(i => i.name === arr[x].id.substr(0, 5))
                            if (arr[x].className.baseVal === 'start') {

                                return yScale(arrpoints.scale[1])

                            } else {

                                return yScale(arrpoints.scale[3])
                            }
                        })


                },
                500)

        }
    }

}

var width_focus = 1100,
    margin_bottom = 20,
    height_focus = 100 + margin_bottom;


var xScale_focus = d3.scaleLinear().domain([0, sort_Data.length])
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
        Volume_box.selectAll("*").remove();
        chart_zoom(range_data, selection)

    }
}