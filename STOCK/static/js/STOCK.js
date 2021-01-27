function doSomethingWithData(error, jsondata) {

    const object = JSON.parse(jsondata)
    object.forEach(function (obj) {
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
console.log(sort_Data)
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

var RSI_div = d3.select("#chart")
    .append("div")
    .attr("class", "RSI_box")
var Stochastic_div = d3.select("#chart")
    .append("div")
    .attr("class", "Stochastic_box")


var points = []
var pointsH = []
var SMA_lines = []
var RSI_lines = []
var Stochastic_lines = []



function chart_zoom(range_data, selection) {

    var zoom_off = false;
    var t;
    var xScaleZ;
    var timesClicked = 0;
    var resizeTimer;
    const Volume_height = 100;
    const RSI_height = 100;
    const Stochastic_height = 100;


    if (range_data[0] <= 0) {
        range_data = [0, range_data[1]];
    } else if (range_data[1] >= sort_Data.length) {
        range_data = [range_data[0], sort_Data.length - 1]
    } else if (range_data[0] <= 0 && range_data[1] >= sort_Data.length) {
        range_data = [0, sort_Data.length - 1]
    }

    filtered_data = _.filter(sort_Data, d => ((d.date >= sort_Data[range_data[0]].date) && (d.date <= sort_Data[range_data[1]].date)))
    function Stochastic_data(period, k_slow, d_slow) {
        period = parseInt(period)
        k_slow = parseInt(k_slow)
        d_slow = parseInt(d_slow)
        console.log(period)
        let array_data = []

        let array_max = []
        let array_low = []
        let array_K = []
        let array_K_slow = []
        let first_k = 0
        let first_d = 0

        sort_Data.map((x, i, arr) => {
            if (i < period) {
                array_max.push(x.high)
                array_low.push(x.low)
                array_data.push([0, 0])
                if (array_low.length == period && array_max.length == period) {

                    let val_max = d3.max(array_max)
                    let val_min = d3.min(array_low)
                    let k = (x.close - val_min) / (val_max - val_min) * 100
                    array_K.push(k)
                    array_data.push([0, 0])
                }
            } else {

                array_max.shift()
                array_low.shift()
                array_max.push(x.high)
                array_low.push(x.low)
                let val_max = d3.max(array_max)
                let val_min = d3.min(array_low)
                let k = (x.close - val_min) / (val_max - val_min) * 100

                if (array_K.length <= k_slow) {
                    first_k++
                    array_K.push(k)
                    if (first_k == k_slow) {
                        array_K_slow.push(d3.sum(array_K) / array_K.length)
                        array_data.push([(d3.sum(array_K) / array_K.length), 0])
                    } else {
                        array_data.push([0, 0])
                    }
                } else {
                    array_K.shift()
                    array_K.push(k)
                    if (array_K_slow <= d_slow) {
                        first_d++
                        array_K_slow.push(d3.sum(array_K) / array_K.length)
                        if (first_d == d_slow) {

                            array_data.push([(d3.sum(array_K) / array_K.length), (d3.sum(array_K_slow) / array_K_slow.length)])

                        } else {
                            array_data.push([(d3.sum(array_K) / array_K.length), 0])

                        }

                    } else {
                        array_K_slow.shift()
                        array_K_slow.push(d3.sum(array_K) / array_K.length)
                        array_data.push([(d3.sum(array_K) / array_K.length), (d3.sum(array_K_slow) / array_K_slow.length)])
                    }
                }
            }

        })
        return array_data.slice(range_data[0], range_data[1])
    }
    function RSI_data(period) {
        period = parseInt(period)

        let array_data = []
        let av_up = []
        let av_down = []
        let av_gain = 0
        let av_loss = 0
        sort_Data.map((x, i, arr) => {
            console.log(x.date)
            if (i == 0) {
                av_up.push(0)
                av_down.push(0)
                let RSI = 0
                array_data.push(RSI)

            } else if (i < period) {

                if (arr[i].close > arr[(i - 1)].close) {

                    av_up.push(arr[i].close - arr[(i - 1)].close)
                } else {

                    av_down.push(arr[(i - 1)].close - arr[i].close)
                }
                let RSI = 0
                array_data.push(RSI)
                av_gain = d3.sum(av_up) / period
                av_loss = d3.sum(av_down) / period
                console.log(av_gain)
                console.log(av_loss)
                console.log(RSI)

            } else {

                if (arr[i].close > arr[i - 1].close) {
                    av_gain = (av_gain * (period - 1) + (arr[i].close - arr[i - 1].close)) / period
                    console.log(av_gain)
                    av_loss = ((av_loss * (period - 1)) / period)
                    console.log(av_loss)
                } else {

                    av_gain = ((av_gain * (period - 1)) / period)
                    console.log(av_gain)

                    av_loss = ((av_loss * (period - 1) + (arr[i - 1].close - arr[i].close)) / period)
                    console.log(av_loss)
                }
                let RSI = 100 - (100 / (1 + (av_gain / av_loss)))
                console.log(x.date,RSI)
                array_data.push(RSI)
            }

        })

        return array_data.slice(range_data[0], range_data[1])
    }
    function SMA_data(data, data_valu, period) {
        period = parseInt(period)

        let array_data = []
        data.map((x, i, arr) => {
            if (selection[0] > period) {
                if (i < period + 1) {

                    let array_sort = sort_Data.slice(range_data[0] - (period - i), range_data[0]).map(data => data[data_valu])
                    let array = data.slice(0, i).map(data => data[data_valu])
                    let combine = array_sort.concat(array)
                    let sum_data = d3.sum(combine)

                    let SMA = sum_data / combine.length

                    if (isNaN(SMA)) {
                        array_data.push(arr[i + 1][data_valu])


                    } else {

                        array_data.push(SMA)
                    }

                } else {
                    let array = data.slice(i - period, i).map(data => data[data_valu])
                    let sum_data = d3.sum(array)
                    let SMA = sum_data / array.length

                    array_data.push(SMA)

                }

            } else {
                if (i < period + 1) {

                    let array = data.slice(0, i).map(data => data[data_valu])
                    let sum_data = d3.sum(array)
                    let SMA = sum_data / array.length

                    if (isNaN(SMA)) {
                        array_data.push(arr[i + 1][data_valu])

                    } else {
                        array_data.push(SMA)
                    }

                } else {
                    let array = data.slice(i - period, i).map(data => data[data_valu])
                    let sum_data = d3.sum(array)
                    let SMA = sum_data / array.length

                    array_data.push(SMA)

                }


            }


        })
        return array_data
    }


    var xScale = d3.scaleLinear().domain([-1, filtered_data.length+50])
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
    var yScale_volume = d3.scaleLinear().domain([0, d3.max(filtered_data.map((x) => { return x.volume; }))]).range([Volume_height, 0]).nice();
    var yScale_RSI = d3.scaleLinear().domain([-10, 110]).range([RSI_height, 0]).nice();
    var yScale_Stochastic = d3.scaleLinear().domain([0, 100]).range([Stochastic_height, 0]).nice();
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
        .style("fill", "#b3b6b7")


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


    Volume_box.attr("viewBox", [0, 0, width, Volume_height])
        .attr("class", "VolumeView")
       
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
        .subject(function () {
            var t = d3.select(this);

            return { x1: t.attr("x1"), y1: t.attr("y1"), x2: t.attr("x2"), y2: t.attr("y2") };
        })
        .on("start", dragstarted)
        .on('drag', dragLine)
        .on('end', dragended);

    let moveLineH = d3.drag()
        .subject(function () {
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

    let dragP = d3.drag()
        .subject(function () {
            var t = d3.select(this);

            return { cx: t.attr("cx"), cy: t.attr("cy") };
        })
        .on('start', dragstarted)
        .on('drag', draggedP)
        .on('end', dragended);
    if (Stochastic_lines.length >= 1) {
        Stochastic_lines.map((x) => {
            let period = x.period
            let k_slow = x.k_slow
            let d_slow = x.d_slow

            Stochastic_box = Stochastic_div.append("svg:svg")
            Stochastic_box.attr("viewBox", [0, 0, width, Stochastic_height])
                .attr("class", "StochasticView")

            Stochastic_box.append("path")
                .attr("class", "Stochastic_path_K")
                .datum(Stochastic_data(period, k_slow, d_slow))
                .attr("fill", "none")
                .attr("stroke", `red`)
                .attr("stroke-width", 1)
                .attr("d", d3.line()
                    .x((d, i, arr) => {
                        if (xScaleZ) {
                            return xScaleZ(i)
                        } else {
                            return xScale(i)
                        }
                    })
                    .y((d, i, arr) => { return yScale_Stochastic(arr[i][0]) })
                )
            Stochastic_box.append("path")
                .attr("class", "Stochastic_path_D")
                .datum(Stochastic_data(period, k_slow, d_slow))
                .attr("fill", "none")
                .attr("stroke", `blue`)
                .attr("stroke-width", 1)
                .attr("d", d3.line()
                    .x((d, i, arr) => {
                        if (xScaleZ) {
                            return xScaleZ(i)
                        } else {
                            return xScale(i)
                        }
                    })
                    .y((d, i, arr) => { return yScale_Stochastic(arr[i][1]) })
                )
            let line30 = Stochastic_box.append("line")
                .attr("x1", xScale(xScale_focus.domain()[0]))
                .attr("y1", yScale_Stochastic(20))
                .attr("x2", xScale(xScale_focus.domain()[1]))
                .attr("y2", yScale_Stochastic(20))
                .attr("stroke-width", 1)
                .attr("stroke", "black")
                .attr("clip-path", "url(#clip)")

            let line70 = Stochastic_box.append("line")
                .attr("x1", xScale(xScale_focus.domain()[0]))
                .attr("y1", yScale_Stochastic(80))
                .attr("x2", xScale(xScale_focus.domain()[1]))
                .attr("y2", yScale_Stochastic(80))
                .attr("stroke-width", 1)
                .attr("stroke", "black")
                .attr("clip-path", "url(#clip)")

        })
    }
    if (RSI_lines.length >= 1) {
        RSI_lines.map((x) => {
            let color = x.color;
            let period = x.period
            RSI_box = RSI_div.append("svg:svg")
            RSI_box.attr("viewBox", [0, 0, width, RSI_height])
                .attr("class", "RSIView")
            RSI_box.append("path")
                .attr("class", "RSI_path")
                .datum(RSI_data(period))
                .attr("fill", "none")
                .attr("stroke", `${color}`)
                .attr("stroke-width", 1.5)
                .attr("d", d3.line()
                    .x((d, i, arr) => {
                        if (xScaleZ) {
                            return xScaleZ(i)
                        } else {
                            return xScale(i)
                        }
                    })
                    .y((d, i, arr) => { return yScale_RSI(arr[i]) })
                )
            let line30 = RSI_box.append("line")
                .attr("x1", xScale(xScale_focus.domain()[0]))
                .attr("y1", yScale_RSI(30))
                .attr("x2", xScale(xScale_focus.domain()[1]))
                .attr("y2", yScale_RSI(30))
                .attr("stroke-width", 1)
                .attr("stroke", "black")
                .attr("clip-path", "url(#clip)")

            let line70 = RSI_box.append("line")
                .attr("x1", xScale(xScale_focus.domain()[0]))
                .attr("y1", yScale_RSI(70))
                .attr("x2", xScale(xScale_focus.domain()[1]))
                .attr("y2", yScale_RSI(70))
                .attr("stroke-width", 1)
                .attr("stroke", "black")
                .attr("clip-path", "url(#clip)")

        })
    }
    if (SMA_lines.length >= 1) {
        SMA_lines.map((x) => {

            let color = x.color
            let period = x.period
            let data_value = x.data_value

            chart.append("path")
                .attr("class", "SMA_path")
                .datum(SMA_data(filtered_data, data_value, period))
                .attr("fill", "none")
                .attr("stroke", `${color}`)
                .attr("stroke-width", 1.5)
                .attr("d", d3.line()
                    .x((d, i, arr) => {
                        if (xScaleZ) {
                            return xScaleZ(i)
                        } else {
                            return xScale(i)
                        }
                    })
                    .y((d, i, arr) => { return yScale(arr[i]) })

                )
        })
    }
    if (points.length >= 1) {
        points.map((x) => {

            var name = x.name

            if (name.substr(0, 5) === "LineH") {
                var tradingLIne = chart.append("g")
                    .attr("class", "HorizontalLIne")
                var line_trend = tradingLIne.append("line")
                    .attr("id", `${x.name}`)
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
                    .attr("id", `${x.name}`)
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

                if (x.name.includes("P", 4)) {
                    circles1
                        .call(dragP)
                } else {
                    circles1
                        .call(drag);

                }


                circles2 = tradingLIne.append('circle')
                    .attr("id", `${x.name}End`)
                    .attr('class', 'End')
                    .attr('r', 2.0)
                    .attr('cx', xScale((x.scale[2] - xScale_focus.invert(selection[0]))))
                    .attr('cy', yScale(x.scale[3]))
                    .style('cursor', 'pointer')
                    .style('fill', "black")

                if (x.name.includes("P", 4)) {
                    circles2
                        .call(dragP)
                } else {
                    circles2
                        .call(drag);

                }
            }
        })

    }


    const extent = [
        [0, 0],
        [width, height]
    ];


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
        .style("top", "100px")
        .attr("class", "dropdown")
    var divButton1 = d3.select("#chart")
        .append("div")
        .style("position", "absolute")
        .style("right", "16%")
        .style("top", "100px")
        .attr("class", "dropdown")
    var lineButton = divButton.append("button")
        .attr("type", "button")
        .attr("class", "btn-btn")
        .text("linia")
        .on('click', drop)
    var funcButton = divButton1.append("button")
        .attr("type", "button")
        .attr("class", "btn-btn")
        .text("f(x)")
        .on('click', drop)
    var content = divButton.append("div")
        .attr("class", "dropdown-content")
        .attr("id", "myDropdow")
    var contentFx = divButton1.append("div")
        .attr("class", "dropdown-content")
        .attr("id", "myDropdow")
    var button_SMA = contentFx.append("p")
        .attr("type", "button")
        .attr("class", "btn-cont")
        .style("text-align", "left")
        .text("SMA")
        .on('click', SMA_panel)

    var button_RSI = contentFx.append("p")
        .attr("type", "button")
        .attr("class", "btn-cont")
        .style("text-align", "left")
        .text("RSI")
        .on('click', RSI_panel)
    var button_Stochastic = contentFx.append("p")
        .attr("type", "button")
        .attr("class", "btn-cont")
        .style("text-align", "left")
        .text("Stochastic")
        .on('click', Stochastic_panel)

    var button_line = content.append("p")
        .attr("type", "button")
        .attr("class", "btn-cont")
        .text("linia")
        .on('click', createDot)
    var button_horizontal = content.append("p")
        .attr("type", "button")
        .attr("class", "btn-cont")
        .text("pozioma")
        .on('click', lineHorizontal)
    var button_parallel = content.append("p")
        .attr("type", "button")
        .attr("class", "btn-cont")
        .text("równoległa")
        .on('click', lineParallel)
    var cross = d3.select("#chart")
        .append("button")
        .attr("type", "button")
        .attr("class", "btn-btn")
        .style("position", "absolute")
        .style("right", "14%")
        .style("top", "100px")
        .on('click', cross)
        .append("i")
        .attr("class", "fa fa-crosshairs")

    function drop() {
        timesClicked++;
        destroy_CROSS()

        var Parent_div = this.parentNode

        if (timesClicked > 1) {
            let all = d3.selectAll(".dropdown-content")
            all.attr("class", "dropdown-content")
            timesClicked = 0
        } else {
            Parent_div.childNodes[1].classList.toggle("show");
        }
    }
    var drag_start = []
    var line_Pdrag = []

    function dragstarted() {
        zoom_off = true
        var x = d3.event.x;
        var y = d3.event.y;
        drag_start.push(x, y)
        let line = d3.select(`#${this.id.substr(0, 8)}`)


        if (this.id.substr(0, 8).substr(-1) == '1' && line.attr("id").length === 8) {
            console.log(this.id.substr(0, 8).substr(-1))

            let secend_line = d3.select(`#${this.id.substr(0, 7)}2`)


            line_Pdrag.push(secend_line._groups[0][0].x1.baseVal.value, secend_line._groups[0][0].y1.baseVal.value,
                secend_line._groups[0][0].x2.baseVal.value, secend_line._groups[0][0].y2.baseVal.value)

        } else if (this.id.substr(0, 8).substr(-1) == '2' && line.attr("id").length === 8) {

            let secend_line = d3.select(`#${this.id.substr(0, 7)}1`)


            line_Pdrag.push(secend_line._groups[0][0].x1.baseVal.value, secend_line._groups[0][0].y1.baseVal.value,
                secend_line._groups[0][0].x2.baseVal.value, secend_line._groups[0][0].y2.baseVal.value)

        }

    }

    function dragged() {
        var cx = d3.event.x;
        var cy = d3.event.y;
        d3.select(this)
            .attr('cx', cx)
            .attr('cy', cy)

        var linia_drag = d3.select(`#${this.id.substr(0, 5)} `)
        var arrpoints = points.find(x => x.name === this.id.substr(0, 5))

        if (this.className.baseVal === 'start') {

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

    function draggedP() {
        var cx = d3.event.x;
        var cy = d3.event.y;

        d3.select(this)
            .attr('cx', cx)
            .attr('cy', cy)
        var linename = this.id.substr(0, 8)

        var linia_drag = d3.select(`#${linename} `)
        var arrpoints = points.find(x => x.name === linename)


        if (this.className.baseVal === 'start') {

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

            if (this.id.substr(0, 8).substr(-1) === '1') {

                var linia_drag1 = d3.select(`#${this.id.substr(0, 7)}2`)
                var circle = d3.select(`#${this.id.substr(0, 7)}2Start`)

                var x1 = line_Pdrag[0]

                var y1 = line_Pdrag[1]
                console.log(line_Pdrag)
                linia_drag1
                    .attr('x1', (x1 + (cx - d3.event.subject.cx)))
                    .attr('y1', (y1 + (cy - d3.event.subject.cy)))
                circle
                    .attr('cx', (x1 + (cx - d3.event.subject.cx)))
                    .attr('cy', (y1 + (cy - d3.event.subject.cy)))
                var arrpoints1 = points.find(x => x.name === `${this.id.substr(0, 7)}2`)
                console.log(arrpoints1)
                if (xScaleZ) {
                    arrpoints1.scale[0] = xScaleZ.invert((x1 + (cx - d3.event.subject.cx))) + xScale_focus.invert(selection[0])
                    arrpoints1.scale[1] = yScale.invert((y1 + (cy - d3.event.subject.cy)))
                } else {
                    arrpoints1.scale[0] = xScale.invert((x1 + (cx - d3.event.subject.cx))) + xScale_focus.invert(selection[0])
                    arrpoints1.scale[1] = yScale.invert((y1 + (cy - d3.event.subject.cy)))
                }
            } else if (this.id.substr(0, 8).substr(-1) === '2') {
                console.log(this.id.substr(0, 8).substr(-1))

                var linia_drag1 = d3.select(`#${this.id.substr(0, 7)}1`)
                var circle = d3.select(`#${this.id.substr(0, 7)}1Start`)

                var x1 = line_Pdrag[0]
                var y1 = line_Pdrag[1]

                linia_drag1
                    .attr('x1', (x1 + (cx - d3.event.subject.cx)))
                    .attr('y1', (y1 + (cy - d3.event.subject.cy)))
                circle
                    .attr('cx', (x1 + (cx - d3.event.subject.cx)))
                    .attr('cy', (y1 + (cy - d3.event.subject.cy)))

                var arrpoints1 = points.find(x => x.name === `${this.id.substr(0, 7)}1`)
                if (xScaleZ) {
                    arrpoints1.scale[0] = xScaleZ.invert((x1 + (cx - d3.event.subject.cx))) + xScale_focus.invert(selection[0])
                    arrpoints1.scale[1] = yScale.invert((y1 + (cy - d3.event.subject.cy)))
                } else {
                    arrpoints1.scale[0] = xScale.invert((x1 + (cx - d3.event.subject.cx))) + xScale_focus.invert(selection[0])
                    arrpoints1.scale[1] = yScale.invert((y1 + (cy - d3.event.subject.cy)))
                }
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
            if (this.id.substr(0, 8).substr(-1) === '1') {
                console.log(this.id.substr(0, 8).substr(-1))

                var linia_drag1 = d3.select(`#${this.id.substr(0, 7)}2`)
                var circle = d3.select(`#${this.id.substr(0, 7)}2End`)

                var x2 = line_Pdrag[2]
                var y2 = line_Pdrag[3]

                linia_drag1
                    .attr('x2', (x2 + (cx - d3.event.subject.cx)))
                    .attr('y2', (y2 + (cy - d3.event.subject.cy)))
                circle
                    .attr('cx', (x2 + (cx - d3.event.subject.cx)))
                    .attr('cy', (y2 + (cy - d3.event.subject.cy)))
                var arrpoints1 = points.find(x => x.name === `${this.id.substr(0, 7)}2`)
                if (xScaleZ) {
                    arrpoints1.scale[2] = xScaleZ.invert((x2 + (cx - d3.event.subject.cx))) + xScale_focus.invert(selection[0])
                    arrpoints1.scale[3] = yScale.invert((y2 + (cy - d3.event.subject.cy)))
                } else {
                    arrpoints1.scale[2] = xScale.invert((x2 + (cx - d3.event.subject.cx))) + xScale_focus.invert(selection[0])
                    arrpoints1.scale[3] = yScale.invert((y2 + (cy - d3.event.subject.cy)))
                }
            } else if (this.id.substr(0, 8).substr(-1) === '2') {


                var linia_drag1 = d3.select(`#${this.id.substr(0, 7)}1`)
                var circle = d3.select(`#${this.id.substr(0, 7)}1End`)

                var x2 = line_Pdrag[2]
                var y2 = line_Pdrag[3]

                linia_drag1
                    .attr('x2', (x2 + (cx - d3.event.subject.cx)))
                    .attr('y2', (y2 + (cy - d3.event.subject.cy)))
                circle
                    .attr('cx', (x2 + (cx - d3.event.subject.cx)))
                    .attr('cy', (y2 + (cy - d3.event.subject.cy)))

                var arrpoints1 = points.find(x => x.name === `${this.id.substr(0, 7)}1`)
                if (xScaleZ) {
                    arrpoints1.scale[2] = xScaleZ.invert((x2 + (cx - d3.event.subject.cx))) + xScale_focus.invert(selection[0])
                    arrpoints1.scale[3] = yScale.invert((y2 + (cy - d3.event.subject.cy)))
                } else {
                    arrpoints1.scale[2] = xScale.invert((x2 + (cx - d3.event.subject.cx))) + xScale_focus.invert(selection[0])
                    arrpoints1.scale[3] = yScale.invert((y2 + (cy - d3.event.subject.cy)))
                }
            }
        }

    }

    function dragLineH() {
        var x = d3.event.x;
        var y = d3.event.y;


        var Ny = drag_start[1] - y

        var line_drag = d3.select(this);
        var arrpoints = points.find(x => x.name === this.id.substr(0, 6))

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

    function Stochastic() {
        console.log("Stochastic")
        let period = document.getElementById("period_Stochastic").value
        let d_slow = document.getElementById("D_slow_Stochastic").value
        let k_slow = document.getElementById("K_slow_Stochastic").value
        console.log(period)
        console.log(d_slow)
        console.log(k_slow)

        Stochastic_lines.shift()
        Stochastic_div.selectAll("*").remove();

        Stochastic_lines.push({
            "period": period,
            "d_slow": d_slow,
            "k_slow": k_slow
        })

        Stochastic_box = Stochastic_div.append("svg:svg")
        Stochastic_box.attr("viewBox", [0, 0, width, Stochastic_height])
            .attr("class", "StochasticView")

        Stochastic_box.append("path")
            .attr("class", "Stochastic_path_K")
            .datum(Stochastic_data(period, k_slow, d_slow))
            .attr("fill", "none")
            .attr("stroke", `red`)
            .attr("stroke-width", 1)
            .attr("d", d3.line()
                .x((d, i, arr) => {
                    if (xScaleZ) {
                        return xScaleZ(i)
                    } else {
                        return xScale(i)
                    }
                })
                .y((d, i, arr) => { return yScale_Stochastic(arr[i][0]) })
            )
        Stochastic_box.append("path")
            .attr("class", "Stochastic_path_D")
            .datum(Stochastic_data(period, k_slow, d_slow))
            .attr("fill", "none")
            .attr("stroke", `blue`)
            .attr("stroke-width", 1)
            .attr("d", d3.line()
                .x((d, i, arr) => {
                    if (xScaleZ) {
                        return xScaleZ(i)
                    } else {
                        return xScale(i)
                    }
                })
                .y((d, i, arr) => { return yScale_Stochastic(arr[i][1]) })
            )
        let line30 = Stochastic_box.append("line")
            .attr("x1", xScale(xScale_focus.domain()[0]))
            .attr("y1", yScale_Stochastic(20))
            .attr("x2", xScale(xScale_focus.domain()[1]))
            .attr("y2", yScale_Stochastic(20))
            .attr("stroke-width", 1)
            .attr("stroke", "black")
            .attr("clip-path", "url(#clip)")

        let line70 = Stochastic_box.append("line")
            .attr("x1", xScale(xScale_focus.domain()[0]))
            .attr("y1", yScale_Stochastic(80))
            .attr("x2", xScale(xScale_focus.domain()[1]))
            .attr("y2", yScale_Stochastic(80))
            .attr("stroke-width", 1)
            .attr("stroke", "black")
            .attr("clip-path", "url(#clip)")



        d3.select(".Stochastic_panel").remove()
        timesClicked = 0
    }
    function RSI() {
        console.log("rsi")
        let color = d3.select("#color_RSI").property("value")
        let period = document.getElementById("period_RSI").value
        console.log(period)
        console.log(color)
        RSI_lines.shift()
        RSI_div.selectAll("*").remove();

        RSI_lines.push({
            "color": color,
            "period": period
        })

        RSI_box = RSI_div.append("svg:svg")
        RSI_box.attr("viewBox", [0, 0, width, RSI_height])
            .attr("class", "RSIView")

        RSI_box.append("path")
            .attr("class", "RSI_path")
            .datum(RSI_data(period))
            .attr("fill", "none")
            .attr("stroke", `${color}`)
            .attr("stroke-width", 1.5)
            .attr("d", d3.line()
                .x((d, i, arr) => {
                    if (xScaleZ) {
                        return xScaleZ(i)
                    } else {
                        return xScale(i)
                    }
                })
                .y((d, i, arr) => { return yScale_RSI(arr[i]) })
            )
        let line30 = RSI_box.append("line")
            .attr("x1", xScale(xScale_focus.domain()[0]))
            .attr("y1", yScale_RSI(30))
            .attr("x2", xScale(xScale_focus.domain()[1]))
            .attr("y2", yScale_RSI(30))
            .attr("stroke-width", 1)
            .attr("stroke", "black")
            .attr("clip-path", "url(#clip)")

        let line70 = RSI_box.append("line")
            .attr("x1", xScale(xScale_focus.domain()[0]))
            .attr("y1", yScale_RSI(70))
            .attr("x2", xScale(xScale_focus.domain()[1]))
            .attr("y2", yScale_RSI(70))
            .attr("stroke-width", 1)
            .attr("stroke", "black")
            .attr("clip-path", "url(#clip)")



        d3.select(".RSI_panel").remove()
        timesClicked = 0
    }

    function SMA() {

        let color = d3.select("#color_SMA").property("value")
        let period = document.getElementById("period_SMA").value
        let data_value = document.getElementById("select_data_SMA").value
        var length_class = d3.selectAll(".SMA_path")

        var name = "SMA" + (length_class._groups[0].length + 1)
        SMA_lines.push({
            "name": name,
            "color": color,
            "data_value": data_value,
            "period": period
        })


        chart.append("path")
            .attr("class", "SMA_path")
            .datum(SMA_data(filtered_data, data_value, period))
            .attr("fill", "none")
            .attr("stroke", `${color}`)
            .attr("stroke-width", 1.5)
            .attr("d", d3.line()
                .x((d, i, arr) => {
                    if (xScaleZ) {
                        return xScaleZ(i)
                    } else {
                        return xScale(i)
                    }
                })
                .y((d, i, arr) => { return yScale(arr[i]) })

            )
        d3.select(".SMA_panel").remove()
        timesClicked = 0
    }

    function dragLine() {
        var x = d3.event.x;
        var y = d3.event.y;

        var Nx = drag_start[0] - x
        var Ny = drag_start[1] - y

        var line_drag = d3.select(this);
        var arrpoints = points.find(x => x.name === this.id)

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
        line_Pdrag = []

    }


    var cross_click = 0

    function Stochastic_panel() {
        contentFx.attr("class", "dropdown-content")


        let pos_div = []
        let isDown = false;

        let drag_panel = d3.drag()
            .subject(function () {
                let pos = d3.select(".Stochastic_panel").node().getBoundingClientRect();

                return { x: pos.x, y: pos.y, };
            })
            .on('start', dragged_panelstart)
            .on('drag', dragged_panel)
            .on('end', dragged_panelend)

        function dragged_panelstart() {

            if (d3.event.sourceEvent.target === this || d3.event.sourceEvent.target === row1._groups[0][0]) {

                let x = d3.event.x;
                let y = d3.event.y;
                pos_div.push(x, y)

                isDown = true
            }

        }

        function dragged_panel() {

            if (isDown) {

                let x = d3.event.x;
                let y = d3.event.y;

                Nx = pos_div[0] - x
                Ny = pos_div[1] - y
                SMA_div = d3.selectAll(".Stochastic_panel")
                    .style("left", (d3.event.subject.x - Nx) + "px")
                    .style("top", (d3.event.subject.y - Ny) + "px")
            }

        }
        function dragged_panelend() {

            isDown = false
        }
        function destroy() {
            panel.remove()
            timesClicked = 0
        }
        let panel = d3.select(".training-container")
            .append("div")
            .style("position", "absolute")
            .style("left", "45%")
            .style("top", "200px")
            .style("background-color", "grey")
            .style("width", "250px")
            .style("height", "250px")
            .attr("class", "Stochastic_panel")
            .attr("id", "Stochastic_panel")
            .call(drag_panel)

        let row1 = panel.append("div")
            .style("width", "100%")
            .style("padding", "10px 5px 15px 15px")
            .style("background-color", "#1f1f20")
        row1
            .append("span")
            .style("color", "white")
            .text("Stochastic oscillator")
        row1
            .append("span")
            .style("float", "right")
            .style("margin-top", "-5px")
            .style("margin-right", "3%")
            .on('click', destroy)
            .append("i")
            .attr("class", "fa fa-times")
            .style("color", "white")
            .style("cursor", "pointer")

        let row2 = panel.append("div")
            .style("width", "100%")
            .style("display", "block")
        let row3 = panel.append("div")
            .style("width", "100%")
            .style("display", "block")
        let div1 = row2.append("div")
            .style("display", "table-cell")
            .style("padding", "5px 10px")
            .style("width", "50%")
        let div2 = row3.append("div")
            .style("display", "table-cell")
            .style("padding", "5px 10px")
            .style("width", "50%")
        let div3 = row3.append("div")
            .style("display", "table-cell")
            .style("padding", "5px 10px")
            .style("width", "50%")


        div1
            .append("label")
            .style("padding-left", "15px")
            .text("Okres")
        let input_period = div1.append("input")
            .attr("id", "period_Stochastic")
            .attr("type", "number")
            .style("width", "100%")
            .style("height", "30px")
            .style("background-color", "#152126")
            .style("border", "solid 1px #2b3a42")
            .style("color", "white")
            .attr("value", "10")
        input_period
            .on("mousedown", function () { d3.event.stopPropagation(); })

        div2
            .append("label")
            .style("padding-left", "15px")
            .text("K Slow")
        div3
            .append("label")
            .style("padding-left", "15px")
            .text("D Slow")
        let input_K_slow = div2.append("input")
            .attr("id", "K_slow_Stochastic")
            .attr("type", "number")
            .style("width", "100%")
            .style("height", "30px")
            .style("background-color", "#152126")
            .style("border", "solid 1px #2b3a42")
            .style("color", "white")
            .attr("value", "3")
        let input_D_slow = div3.append("input")
            .attr("id", "D_slow_Stochastic")
            .attr("type", "number")
            .style("width", "100%")
            .style("height", "30px")
            .style("background-color", "#152126")
            .style("border", "solid 1px #2b3a42")
            .style("color", "white")
            .attr("value", "3")
        input_K_slow
            .on("mousedown", function () { d3.event.stopPropagation(); })


        let row4 = panel.append("div")
            .style("width", "100%")
            .style("display", "flex")
        let div4 = row4.append("div")
            .style("padding", "15px")
            .style("width", "70%")
            .style("margin", "auto")

        div4
            .append("button")
            .attr("type", "button")
            .text("Zastosuj")
            .style("width", "100%")
            .style("color", "white")
            .style("background-color", "#00b276")
            .on('click', Stochastic)

    }

    function RSI_panel() {
        contentFx.attr("class", "dropdown-content")


        let pos_div = []
        let isDown = false;

        let drag_panel = d3.drag()
            .subject(function () {
                let pos = d3.select(".RSI_panel").node().getBoundingClientRect();

                return { x: pos.x, y: pos.y, };
            })
            .on('start', dragged_panelstart)
            .on('drag', dragged_panel)
            .on('end', dragged_panelend)

        function dragged_panelstart() {

            if (d3.event.sourceEvent.target === this || d3.event.sourceEvent.target === row1._groups[0][0]) {

                let x = d3.event.x;
                let y = d3.event.y;
                pos_div.push(x, y)

                isDown = true
            }

        }

        function dragged_panel() {

            if (isDown) {

                let x = d3.event.x;
                let y = d3.event.y;

                Nx = pos_div[0] - x
                Ny = pos_div[1] - y
                SMA_div = d3.selectAll(".RSI_panel")
                    .style("left", (d3.event.subject.x - Nx) + "px")
                    .style("top", (d3.event.subject.y - Ny) + "px")
            }

        }
        function dragged_panelend() {

            isDown = false
        }
        function destroy() {
            panel.remove()
            timesClicked = 0
        }
        let panel = d3.select(".training-container")
            .append("div")
            .style("position", "absolute")
            .style("left", "45%")
            .style("top", "200px")
            .style("background-color", "grey")
            .style("width", "250px")
            .style("height", "250px")
            .attr("class", "RSI_panel")
            .attr("id", "RSI_panel")
            .call(drag_panel)

        let row1 = panel.append("div")
            .style("width", "100%")
            .style("padding", "10px 5px 15px 15px")
            .style("background-color", "#1f1f20")
        row1
            .append("span")
            .style("color", "white")
            .text("Wskaźnik siły RSI")
        row1
            .append("span")
            .style("float", "right")
            .style("margin-top", "-5px")
            .style("margin-right", "3%")
            .on('click', destroy)
            .append("i")
            .attr("class", "fa fa-times")
            .style("color", "white")
            .style("cursor", "pointer")

        let row2 = panel.append("div")
            .style("width", "100%")
            .style("display", "block")
        let div1 = row2.append("div")
            .style("display", "table-cell")
            .style("padding", "5px 10px")
            .style("width", "50%")

        div1
            .append("label")
            .style("padding-left", "15px")
            .text("Okres")
        let input_period = div1.append("input")
            .attr("id", "period_RSI")
            .attr("type", "number")
            .style("width", "100%")
            .style("height", "30px")
            .style("background-color", "#152126")
            .style("border", "solid 1px #2b3a42")
            .style("color", "white")
            .attr("value", "10")
        input_period
            .on("mousedown", function () { d3.event.stopPropagation(); })



        let row3 = panel.append("div")
            .style("width", "100%")
            .style("display", "flex")
        let div4 = row3.append("div")
            .style("padding", "15px")
            .style("width", "70%")
            .style("margin", "auto")
        div1
            .append("label")
            .style("padding-left", "15px")
            .text("Kolor")
        let input_color = div1.append("input")
            .attr("type", "color")
            .attr("id", "color_RSI")
            .style("width", "100%")
            .style("height", "30px")
            .style("background-color", "#152126")
            .style("border", "solid 1px #2b3a42")
            .attr("value", "#FFA200")

        div4
            .append("button")
            .attr("type", "button")
            .text("Zastosuj")
            .style("width", "100%")
            .style("color", "white")
            .style("background-color", "#00b276")
            .on('click', RSI)

    }



    function SMA_panel() {
        contentFx.attr("class", "dropdown-content")
        let SMA_options = ["high", "low", "open", "close"];

        let pos_div = []
        let isDown = false;

        let drag_panel = d3.drag()
            .subject(function () {
                let pos = d3.select(".SMA_panel").node().getBoundingClientRect();

                return { x: pos.x, y: pos.y, };
            })
            .on('start', dragged_panelstart)
            .on('drag', dragged_panel)
            .on('end', dragged_panelend)

        function dragged_panelstart() {

            if (d3.event.sourceEvent.target === this || d3.event.sourceEvent.target === row1._groups[0][0]) {

                let x = d3.event.x;
                let y = d3.event.y;
                pos_div.push(x, y)

                isDown = true
            }

        }

        function dragged_panel() {

            if (isDown) {

                let x = d3.event.x;
                let y = d3.event.y;

                Nx = pos_div[0] - x
                Ny = pos_div[1] - y
                SMA_div = d3.selectAll(".SMA_panel")
                    .style("left", (d3.event.subject.x - Nx) + "px")
                    .style("top", (d3.event.subject.y - Ny) + "px")
            }

        }
        function dragged_panelend() {

            isDown = false
        }
        function destroy() {
            panel.remove()
            timesClicked = 0
        }
        let panel = d3.select(".training-container")
            .append("div")
            .style("position", "absolute")
            .style("left", "45%")
            .style("top", "200px")
            .style("background-color", "grey")
            .style("width", "250px")
            .style("height", "210px")
            .attr("class", "SMA_panel")
            .attr("id", "SMA_panel")
            .call(drag_panel)

        let row1 = panel.append("div")
            .style("width", "100%")
            .style("padding", "10px 5px 15px 15px")
            .style("background-color", "#1f1f20")
        row1
            .append("span")
            .style("color", "white")
            .text("Śednia krocząca SMA")
        row1
            .append("span")
            .style("float", "right")
            .style("margin-top", "-5px")
            .style("margin-right", "3%")
            .on('click', destroy)
            .append("i")
            .attr("class", "fa fa-times")
            .style("color", "white")
            .style("cursor", "pointer")

        let row2 = panel.append("div")
            .style("width", "100%")
            .style("display", "block")
        let div1 = row2.append("div")
            .style("display", "table-cell")
            .style("padding", "5px 10px")
            .style("width", "50%")
        let div2 = row2.append("div")
            .style("display", "table-cell")
            .style("padding", "5px 10px")
            .style("width", "50%")
        div1
            .append("label")
            .style("padding-left", "15px")
            .text("Okres")
        let input_period = div1.append("input")
            .attr("id", "period_SMA")
            .attr("type", "number")
            .style("width", "100%")
            .style("height", "30px")
            .style("background-color", "#152126")
            .style("border", "solid 1px #2b3a42")
            .style("color", "white")
            .attr("value", "10")
        input_period
            .on("mousedown", function () { d3.event.stopPropagation(); })
        div2
            .append("label")
            .text("W oparciu o")
        let selection = div2.append("select")
            .style("width", "100%")
            .attr("id", "select_data_SMA")
            .style("height", "30px")
            .style("background-color", "#152126")
            .style("border", "solid 1px #2b3a42")
            .style("color", "white")
        let options = selection.selectAll("option")
            .data(SMA_options)
            .enter()
            .append("option");


        options.text(function (d) {
            return d;
        })
            .attr("value", function (d) {
                return d;
            });
        let row3 = panel.append("div")
            .style("width", "100%")
            .style("display", "flex")
        let div3 = row3.append("div")
            .style("padding", "5px 10px")
            .style("width", "50%")
        let div4 = row3.append("div")
            .style("padding", "35px 5px 5px 20px")
            .style("width", "45%")
        div3
            .append("label")
            .style("padding-left", "15px")
            .text("Kolor")
        let input_color = div3.append("input")
            .attr("type", "color")
            .attr("id", "color_SMA")
            .style("width", "100%")
            .style("height", "30px")
            .style("background-color", "#152126")
            .style("border", "solid 1px #2b3a42")
            .attr("value", "#FFA200")

        div4
            .append("button")
            .attr("type", "button")
            .style("padding-left", "20px")
            .text("Zastosuj")
            .style("color", "white")
            .style("background-color", "#00b276")
            .on('click', SMA)




    }

    function cross() {
        let all = d3.selectAll(".dropdown-content")
        let div = d3.select("#rect");

        all.attr("class", "dropdown-content")
        timesClicked = 0

        cross_click++

        if (cross_click < 2) {
            div.on("click", function () {
                var m = d3.mouse(this);
                let panel = d3.select("#chart")
                    .append("div")
                    .style("position", "absolute")
                    .style("left", "0.5%")
                    .style("top", "50px")
                    .style("background-color", "grey")
                    .style("width", "120px")
                    .style("height", "200px")
                    .attr("class", "panel")
                let table = panel.append('table')

                let row1 = table.append('tr')
                row1
                    .append('th')
                    .style("color", "white")
                    .text('open')

                row1
                    .append('th')
                    .text('close')
                    .style("color", "white")
                let row2 = table.append('tr')
                let open_th = row2.append('th')
                    .text(`${(Number(xDateScale(Math.floor(xScale.invert(m[0]))).open).toFixed(3))}`)
                    .style("color", "white")
                let close_th = row2.append('th')
                    .text(`${(Number(xDateScale(Math.floor(xScale.invert(m[0]))).close).toFixed(3))}`)
                    .style("color", "white")
                let row3 = table.append('tr')
                row3
                    .append('th')
                    .text('high')
                    .style("color", "white")
                row3
                    .append('th')
                    .text('low')
                    .style("color", "white")
                let row4 = table.append('tr')
                let high_th = row4.append('th')
                    .text(`${(Number(xDateScale(Math.floor(xScale.invert(m[0]))).high).toFixed(3))}`)
                    .style("color", "white")
                let low_th = row4.append('th')
                    .text(`${(Number(xDateScale(Math.floor(xScale.invert(m[0]))).low).toFixed(3))}`)
                    .style("color", "white")
                let row5 = table.append('tr')
                row5
                    .append('th')
                    .text('Volume')
                    .style("color", "white")

                let Volume_th = panel.append('span')
                    .text(`${xDateScale(Math.floor(xScale.invert(m[0]))).low}`)
                    .style("font-family", "sans-serif")
                    .style("font-size", "12px")
                    .style("color", "white")



                let cross_line_x = chart.append("g")
                    .attr("class", "crossx")
                let line_cross_x = cross_line_x.append("line")
                    .attr("x1", 30)
                    .attr("y1", m[1])
                    .attr("x2", xScale(xScale_focus.domain()[1]))
                    .attr("y2", m[1])
                    .attr("stroke-width", 0.7)
                    .attr("stroke", "grey")
                    .attr("clip-path", "url(#clip)")

                let rect_line = cross_line_x.append('rect')
                    .attr('width', 55)
                    .attr('height', 20)
                    .attr("fill", 'grey')
                    .attr("x", 0)
                    .attr("y", m[1] - 10)

                let text_x = cross_line_x.append('text')
                    .attr("x", 5)
                    .attr("dy", m[1] + 7)
                    .attr("font-family", "sans-serif")
                    .attr("font-size", "14px")
                    .attr("fill", "white")
                    .text(`${Number(yScale.invert(m[1]).toFixed(1))}`)

                let cross_line_y = chart.append("g")
                    .attr("class", "crossy")
                    .append("line")
                    .attr("x1", m[0])
                    .attr("y1", yScale(0))
                    .attr("x2", m[0])
                    .attr("y2", yScale(width))
                    .attr("stroke-width", 0.7)
                    .attr("stroke", "grey")


                let Volume_line_y = Volume_box.append('g')
                    .attr("class", "crossVolmeY")
                let line_volume_y = Volume_line_y.append("line")
                    .attr("x1", m[0])
                    .attr("y1", yScale_volume(0))
                    .attr("x2", m[0])
                    .attr("y2", yScale_volume(Volume_height))
                    .attr("stroke-width", 0.7)
                    .attr("stroke", "grey")
                let rect_y = Volume_line_y.append('rect')
                    .attr('width', 100)
                    .attr('height', 20)
                    .attr("fill", 'grey')
                    .attr("x", m[0] - 50)
                    .attr("y", 0)
                let text_y = Volume_line_y.append('text')
                    .attr("x", m[0] - 35)
                    .attr("y", 15)
                    .attr("font-family", "sans-serif")
                    .attr("font-size", "14px")
                    .attr("fill", "white")
                    .text(`${dayjs(xDateScale(Math.floor(xScale.invert(m[0]))).date).format('DD/MM/YYYY')}`)
                if (RSI_lines.length >= 1) {
                    let RSI_line_y = RSI_box.append('g')
                        .attr("class", "crossRSIY")
                    var line_RSI_y = RSI_line_y.append("line")
                        .attr("x1", m[0])
                        .attr("y1", yScale_RSI(0))
                        .attr("x2", m[0])
                        .attr("y2", yScale_RSI(RSI_height))
                        .attr("stroke-width", 0.7)
                        .attr("stroke", "grey")

                }


                div.on("mousemove", () => {
                    var m = d3.mouse(this);

                    line_cross_x
                        .attr("x1", xScale(xScale_focus.domain()[0]))
                        .attr("y1", m[1])
                        .attr("x2", xScale(xScale_focus.domain()[1]))
                        .attr("y2", m[1])
                    rect_line
                        .attr("x", 0)
                        .attr("y", m[1] - 10)
                    text_x
                        .attr("x", 5)
                        .attr("dy", m[1] + 7)
                        .text(`${Number(yScale.invert(m[1]).toFixed(1))}`)



                    cross_line_y
                        .attr("x1", m[0])
                        .attr("y1", yScale(0))
                        .attr("x2", m[0])
                        .attr("y2", yScale(width))
                    line_volume_y
                        .attr("x1", m[0])
                        .attr("y1", yScale(0))
                        .attr("x2", m[0])
                        .attr("y2", yScale(Volume_height))
                    if (RSI_lines.length >= 1) {
                        line_RSI_y
                            .attr("x1", m[0])
                            .attr("y1", yScale_RSI(0))
                            .attr("x2", m[0])
                            .attr("y2", yScale_RSI(RSI_height))
                    }
                    rect_y
                        .attr("x", m[0] - 50)
                        .attr("y", 0)
                    text_y
                        .attr("x", m[0] - 35)
                        .attr("y", 15)
                    if (xScaleZ) {

                        text_y
                            .text(`${dayjs(xDateScale(Math.floor(xScaleZ.invert(m[0]))).date).format('DD/MM/YYYY')}`)

                    } else {

                        text_y
                            .text(`${dayjs(xDateScale(Math.floor(xScale.invert(m[0]))).date).format('DD/MM/YYYY')}`)
                    }
                    if (xScaleZ) {
                        open_th
                            .text(`${(Number(xDateScale(Math.floor(xScaleZ.invert(m[0]))).open).toFixed(3))}`)
                    } else {
                        open_th
                            .text(`${(Number(xDateScale(Math.floor(xScale.invert(m[0]))).open).toFixed(3))}`)

                    }
                    if (xScaleZ) {
                        close_th
                            .text(`${(Number(xDateScale(Math.floor(xScaleZ.invert(m[0]))).close).toFixed(3))}`)
                    } else {
                        close_th
                            .text(`${(Number(xDateScale(Math.floor(xScale.invert(m[0]))).close).toFixed(3))}`)
                    }
                    if (xScaleZ) {
                        high_th
                            .text(`${(Number(xDateScale(Math.floor(xScaleZ.invert(m[0]))).high).toFixed(3))}`)
                    } else {
                        high_th
                            .text(`${(Number(xDateScale(Math.floor(xScale.invert(m[0]))).high).toFixed(3))}`)
                    }
                    if (xScaleZ) {
                        low_th
                            .text(`${(Number(xDateScale(Math.floor(xScaleZ.invert(m[0]))).low).toFixed(3))}`)
                    } else {
                        low_th
                            .text(`${(Number(xDateScale(Math.floor(xScale.invert(m[0]))).low).toFixed(3))}`)
                    }

                    if (xScaleZ) {
                        Volume_th
                            .text(`${xDateScale(Math.floor(xScaleZ.invert(m[0]))).low}`)
                    } else {
                        Volume_th
                            .text(`${xDateScale(Math.floor(xScale.invert(m[0]))).low}`)
                    }
                })
            })

        } else {
            destroy_CROSS()
            cross_click = 0
            div.on("click", null)
            div.on("mousemove", null)

        }


    }
    function destroy_CROSS() {
        let cross_line_x = chart.selectAll(".crossx").remove()
        let cross_line_y = chart.selectAll(".crossy").remove()
        let Volume_line_y = Volume_box.selectAll(".crossVolmeY").remove()
        if (RSI_lines.length >= 1) {
            let Volume_RSI_y = RSI_box.selectAll(".crossRSIY").remove()
        }
        let Panel = d3.select("#chart").selectAll(".panel").remove()
        cross_click = 0

    }

    function lineHorizontal() {
        content.attr("class", "dropdown-content")
        timesClicked = 0
        zoom_off = true
        vardata_circle = []
        scale_var = []
        let div = d3.select("#rect");

        var length_class = d3.selectAll(".HorizontalLIne")

        var name = "LineH" + (length_class._groups[0].length + 1)
        div.on("click", function () {

            var m = d3.mouse(this);

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
        let div = d3.select("#rect");

        zoom_off = true
        var length_class = d3.selectAll(".tradingLIne")

        var name = "Line" + (length_class._groups[0].length + 1)

        isDrawing = true;
        vardata_circle = []
        scale_var = []

        div.on("click", function () {

            var m = d3.mouse(this);

            vardata_circle.push(m[0], m[1])
            if (xScaleZ) {

                scale_var.push(xScaleZ.invert(m[0]) + xScale_focus.invert(selection[0]), yScale.invert(m[1]))
            } else {

                scale_var.push(xScale.invert(m[0]) + xScale_focus.invert(selection[0]), yScale.invert(m[1]))
            }
            line = chart.append("g")
                .attr("class", "tradingLIne");

            line1 = line.append("line")
                .attr("id", `${name}`)
                .attr("class", "drowLine")
                .attr("x1", m[0])
                .attr("y1", m[1])
                .attr("x2", m[0])
                .attr("y2", m[1])
                .attr("stroke-width", 1)
                .attr("stroke", "black")
                .attr("clip-path", "url(#clip)");





            div.on("mousemove", () => {
                if (isDrawing === true) {
                    var m = d3.mouse(this);
                    line1.attr("x2", m[0])
                        .attr("y2", m[1]);
                    chart.on("click", function () {
                        div.on("mousemove", null)
                        div.on("click", null);
                        chart.on("click", null);
                        vardata_circle.push(m[0], m[1])
                        if (xScaleZ) {
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

                    });
                }

            })

        });


    }

    function lineParallel() {
        content.attr("class", "dropdown-content")
        timesClicked = 0
        let vardata_circle = []
        let vardata_circle1 = []
        let scale_var = []
        let scale_var1 = []
        let div = d3.select("#rect");



        zoom_off = true
        var length_class = d3.selectAll(".ParallelLIne")
        var number_line = length_class._groups[0].length

        var name = "LineP" + (number_line + 1) + '-1'

        isDrawing = true;
        vardata_circle = []
        scale_var = []

        div.on("click", function () {

            var m = d3.mouse(this);

            vardata_circle.push(m[0], m[1])
            if (xScaleZ) {
                scale_var.push(xScaleZ.invert(m[0]) + xScale_focus.invert(selection[0]), yScale.invert(m[1]))
            } else {
                scale_var.push(xScale.invert(m[0]) + xScale_focus.invert(selection[0]), yScale.invert(m[1]))
            }
            line = chart.append("g")
                .attr("class", "ParallelLIne")

            var line1 = line.append("line")
                .attr("id", `${name}`)
                .attr("class", "drowLine")
                .attr("x1", m[0])
                .attr("y1", m[1])
                .attr("x2", m[0])
                .attr("y2", m[1])
                .attr("stroke-width", 1)
                .attr("stroke", "black")
                .attr("clip-path", "url(#clip)");

            div.on("mousemove", () => {
                if (isDrawing === true) {
                    var n = d3.mouse(this);
                    line1.attr("x2", n[0])
                        .attr("y2", n[1]);
                    chart.on("click", function () {
                        div.on("mousemove", null)
                        div.on("click", null);
                        chart.on("click", null);
                        vardata_circle.push(n[0], n[1])
                        if (xScaleZ) {
                            scale_var.push(xScaleZ.invert(n[0]) + xScale_focus.invert(selection[0]), yScale.invert(n[1]))
                        } else {
                            scale_var.push(xScale.invert(n[0]) + xScale_focus.invert(selection[0]), yScale.invert(n[1]))
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


                        line.selectAll('circle')
                            .call(dragP);
                        line1.style('cursor', 'all-scroll')
                            .call(moveLine)

                        line = chart.append("g")
                            .attr("class", "ParallelLIne")
                        name2 = "LineP" + (number_line + 1) + '-2'
                        var line2 = line.append("line")
                            .attr("id", `${name2}`)
                            .attr("class", "drowLine")
                            .attr("x1", line1.attr("x1"))
                            .attr("y1", line1.attr("y1"))
                            .attr("x2", line1.attr("x2"))
                            .attr("y2", line1.attr("y2"))
                            .attr("stroke-width", 1)
                            .attr("stroke", "black")
                            .attr("clip-path", "url(#clip)")


                        div.on("mousemove", () => {

                            var m = d3.mouse(this);
                            var x = m[0] - n[0]
                            var y = m[1] - n[1]

                            line2
                                .attr("x1", (Number(line1.attr("x1")) + x))
                                .attr("y1", (Number(line1.attr("y1")) + y))
                                .attr("x2", (Number(line1.attr("x2")) + x))
                                .attr("y2", (Number(line1.attr("y2")) + y))

                            chart.on("click", function () {
                                div.on("mousemove", null)
                                div.on("click", null);
                                chart.on("click", null);

                                vardata_circle1.push((Number(line1.attr("x1")) + x), (Number(line1.attr("y1")) + y), (Number(line1.attr("x2")) + x), (Number(line1.attr("y2")) + y))

                                if (xScaleZ) {
                                    scale_var1.push(xScaleZ.invert((Number(line1.attr("x1")) + x)) + xScale_focus.invert(selection[0]), yScale.invert((Number(line1.attr("y1")) + y)),
                                        xScaleZ.invert((Number(line1.attr("x2")) + x)) + xScale_focus.invert(selection[0]), yScale.invert((Number(line1.attr("y2")) + y))
                                    )
                                } else {
                                    scale_var1.push(xScale.invert((Number(line1.attr("x1")) + x)) + xScale_focus.invert(selection[0]), yScale.invert((Number(line1.attr("y1")) + y)),
                                        xScale.invert((Number(line1.attr("x2")) + x)) + xScale_focus.invert(selection[0]), yScale.invert((Number(line1.attr("y2")) + y))
                                    )
                                }
                                points.push({
                                    "name": name2,
                                    "xy": vardata_circle1,
                                    "scale": scale_var1

                                })

                                circles1 = line.append('circle')
                                    .attr("id", `${name2}Start`)
                                    .attr('class', 'start')
                                    .attr('r', 2.0)
                                    .attr('cx', vardata_circle1[0])
                                    .attr('cy', vardata_circle1[1])
                                    .style('cursor', 'pointer')
                                    .style('fill', "black");
                                circles2 = line.append('circle')
                                    .attr("id", `${name2}End`)
                                    .attr('class', 'End')
                                    .attr('r', 2.0)
                                    .attr('cx', vardata_circle1[2])
                                    .attr('cy', vardata_circle1[3])
                                    .style('cursor', 'pointer')
                                    .style('fill', "black");
                                zoom_off = false
                                line.selectAll('circle')
                                    .call(dragP);
                                line2.style('cursor', 'all-scroll')
                                    .call(moveLine)



                            })
                        })

                    });
                }

            })

        });

    }

    function zoomed() {

        if (zoom_off === false) {

            var t = d3.event.transform;

            xScaleZ = t.rescaleX(xScale);

            var line_zoom = chart.selectAll(".drowLine")
                .attr("x1", (line_zoom, x, arr) => {

                    var arrpoints = points.find(i => i.name === arr[x].id)

                    return xScaleZ(arrpoints.scale[0] - xScale_focus.invert(selection[0]))
                })
                .attr("x2", (line_zoom, x, arr) => {
                    var arrpoints = points.find(i => i.name === arr[x].id)

                    return xScaleZ(arrpoints.scale[2] - xScale_focus.invert(selection[0]))
                })
            var Circle_zoom = chart.selectAll('circle')
                .attr("cx", (Circle_zoom, x, arr) => {

                    var arrpoints = points.find(i => i.name === arr[x].id.slice(0, `-${arr[x].className.baseVal.length}`))
                    if (arr[x].className.baseVal === 'start') {

                        return xScaleZ(arrpoints.scale[0] - xScale_focus.invert(selection[0]))

                    } else {

                        return xScaleZ(arrpoints.scale[2] - xScale_focus.invert(selection[0]))
                    }

                })
            var SMA_zoom = chart.selectAll('.SMA_path')
                .attr("d", d3.line()
                    .x((d, i, arr) => {

                        return xScaleZ(i)
                    })
                    .y((d, i, arr) => { return yScale(arr[i]) })

                )
            if (RSI_lines.length >= 1) {
                let RSI_zoom = RSI_box.selectAll('.RSI_path')
                    .attr("d", d3.line()
                        .x((d, i, arr) => {
                            if (xScaleZ) {
                                return xScaleZ(i)
                            } else {
                                return xScale(i)
                            }
                        })
                        .y((d, i, arr) => { return yScale_RSI(arr[i]) }))

            }
            if (Stochastic_lines.length >= 1) {
                let Stochastic_zoom_k = Stochastic_box.selectAll('.Stochastic_path_K')
                    .attr("d", d3.line()
                        .x((d, i, arr) => {
                            if (xScaleZ) {
                                return xScaleZ(i)
                            } else {
                                return xScale(i)
                            }
                        })
                        .y((d, i, arr) => { return yScale_Stochastic(arr[i][0]) })
                    )
                let Stochastic_zoom_d = Stochastic_box.selectAll('.Stochastic_path_D')
                    .attr("d", d3.line()
                        .x((d, i, arr) => {
                            if (xScaleZ) {
                                return xScaleZ(i)
                            } else {
                                return xScale(i)
                            }
                        })
                        .y((d, i, arr) => { return yScale_Stochastic(arr[i][1]) })
                    )

            }


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

            var t = d3.event.transform;

            xScaleZ = t.rescaleX(xScale);
            clearTimeout(resizeTimer)

            resizeTimer = setTimeout(function () {

                var xmin = xDateScale(Math.floor(xScaleZ.domain()[0])).date

                xmax = xDateScale(Math.floor(xScaleZ.domain()[1])).date

                filtered = _.filter(filtered_data, d => ((d.date >= xmin) && (d.date <= xmax)))

                minP = +d3.min(filtered, d => d.low)
                maxP = +d3.max(filtered, d => d.high)
                var buffer = () => {

                    if ((maxP - minP) * 0.1 > 1) {

                        return Math.floor((maxP - minP) * 0.1)
                    } else {

                        return Number(((maxP - minP) * 0.1).toFixed(2))
                    }
                }

                yScale.domain([minP - buffer(), maxP + buffer()])

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

                        var arrpoints = points.find(i => i.name === arr[x].id)

                        return yScale(arrpoints.scale[1])
                    })
                    .attr("y2", (line_zoom, x, arr) => {

                        var arrpoints = points.find(i => i.name === arr[x].id)

                        return yScale(arrpoints.scale[3])
                    })

                var Circle_zoom = chart.selectAll('circle')
                    .attr("cy", (Circle_zoom, x, arr) => {

                        var arrpoints = points.find(i => i.name === arr[x].id.slice(0, `-${arr[x].className.baseVal.length}`))
                        if (arr[x].className.baseVal === 'start') {

                            return yScale(arrpoints.scale[1])

                        } else {

                            return yScale(arrpoints.scale[3])
                        }
                    })
                var SMA_zoom = chart.selectAll('.SMA_path')
                    .attr("d", d3.line()
                        .x((d, i, arr) => {
                            return xScaleZ(i)
                        })
                        .y((d, i, arr) => { return yScale(arr[i]) }))

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
    .y1(function (d) { return yScale_focus(d.high) })
var focus_chart = d3.select("#chart")
    .append("svg:svg")
    .attr("viewBox", [0, 0, width_focus, height_focus + margin_bottom])

focus_chart
    .append("g")
    .attr("id", "g_chart_focus")
    .attr("transform", "translate(" + 0 + "," + 20 + ")");

var gX_focus = focus_chart.append("g")
    .attr("class", "axis x-axis_focus") //Assign "axis" class
    .attr("transform", `translate(0, ${height_focus})`)
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
    .attr("fill", "#b3b6b7")
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

    let selection = d3.event.selection;
    let all = d3.selectAll(".dropdown-content")

    all.attr("class", "dropdown-content")
    timesClicked = 0

    if (!selection) {

        area.call(brush.move, defaultSelection);

    } else {
        range_data = [Math.floor(xScale_focus.invert(selection[0])), Math.floor(xScale_focus.invert(selection[1]))]
        chart.selectAll("*").remove();
        Volume_box.selectAll("*").remove();
        RSI_div.selectAll("*").remove();
        Stochastic_div.selectAll("*").remove();
        d3.selectAll(".panel").remove();

        let new_char = chart_zoom(range_data, selection)
    }
}