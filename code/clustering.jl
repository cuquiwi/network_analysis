using LightGraphs, MetaGraphs, GraphIO
using ParserCombinator #Needed for GML reading

graph_name = "simpledistros.gml"
number_subreddits = 6
infomap_clu = "simpledistros.clu"
write_file = "test.gml"

# Read the graph
g = open(graph_name, "r") do io
    GraphIO.GML.loadgml(io, "graph")
end
g = MetaGraph(g)


# Save GML file
function savegml(io::IO, g)
    println(io,"graph")
    println(io,"[")
    for i = 1:nv(g)
        println(io,"\tnode")
        println(io,"\t[")
        println(io,"\t\tid $i")
        labels = props(g,i)
        for (key, val) in labels
            println(io, "\t\t$key $val")
        end
        println(io,"\t]")
    end
    for e in LightGraphs.edges(g)
        s,t =Tuple(e)
        println(io, "\tedge")
        println(io, "\t[")
        println(io, "\t\tsource $s")
        println(io, "\t\ttarget $t")
        println(io, "\t]")
    end
    println(io, "]")
    return 1
end

function indexesof(x, iter)
    map(y->y[1],filter(y->x==y[0],zip(iter,1:length)))
end

# Louvain algorithm for undirected unweigthed graphs
function louvain_community(g)
    improvements = false
    comunities = 1:nv(g)

    # First phase
    change = true
    while change
        change = false
        m = sum(weights)

        for i =1: nv(g)
            for j in neighbors(g,i)
                comunitynodes = indexesof(comunities[j], comunities)
                sumj = count(i->(i==comunities[j]),comunities)
                
                delta = 0 #TODO 
            end
        end
    end
end


# Read Infomap clustering and tag nodes
println("Infomap clustering...")
for line in eachline(infomap_clu)
    # Ignore comments of clu file
    if startswith(line, "#")
        continue
    end

    x = split(line,r"\s")
    set_prop!(g,parse(Int32,x[1]),:map, x[2])
end

open(write_file, "w") do io
    savegml(io, g)
end
