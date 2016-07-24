function maxOf3(var ardata)
{
    var maxvalue = ardata[0];

    if(ardata[1] > maxvalue)
        maxvalue = ardata[1];

    if(ardata[2] > maxvalue)
        maxvalue = ardata[2];

    return maxvalue;
}