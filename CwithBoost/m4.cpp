
#include <boost/graph/betweenness_centrality.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <vector>
#include <stack>
#include <queue>
#include <boost/property_map/property_map.hpp>
#include <boost/random/uniform_01.hpp>
#include <boost/random/linear_congruential.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/algorithm/string.hpp>
#include <fstream>


const double error_tolerance = 0.001;

typedef boost::property<boost::edge_weight_t, double,
                 boost::property<boost::edge_index_t, std::size_t> > EdgeProperties;  // define edge property : edge weight(double) and edge index(size)

struct weighted_edge
{
  int source, target;
  double weight;
  int sourceCountry, targetCountry;
}; // define an weighted edge struct

struct sample
{
  int companyCode, companyCountry;
}; // define a test sample

//std::vector<weighted_edge>
void readedgelist(std::vector<weighted_edge>* edgeVector, int* vertexCount, int* edgeCount, const std::string& fileLocation)
{

  std::ifstream inStream;
  std::string passphase;
  inStream.open(fileLocation);
  if (inStream.fail())
  {
      std::cout << "Reading file error.";

  }

  int endingNode = 0;
  int edgeCounter = 0;
  while(inStream>>passphase)
  {
  //        cout<<passphase;

      std::vector<std::string> edgeNodesAndWeight;
      boost::split(edgeNodesAndWeight, passphase, [](char c){return c == ',';});

      weighted_edge newEdge;
      newEdge.source = stoi(edgeNodesAndWeight[0]);
      newEdge.target = stoi(edgeNodesAndWeight[1]);
      newEdge.weight = stod(edgeNodesAndWeight[2]);
      newEdge.sourceCountry = stoi(edgeNodesAndWeight[3]);
      newEdge.targetCountry = stoi(edgeNodesAndWeight[4]);

      int largerNode = newEdge.source > newEdge.target ? newEdge.source: newEdge.target;
      endingNode = endingNode > largerNode ? endingNode : largerNode;  // find the max number
      edgeVector->push_back(newEdge);
      edgeCounter++;
  }
  inStream.close();
  std::cout << "file read complete" << '\n';

  *vertexCount = endingNode+1;
  *edgeCount = edgeCounter;
}

void readSampleList(std::vector<sample>* sampleVector, int* sampleCount, const std::string& fileLocation)
{

  std::ifstream inStream;
  std::string passphase;
  inStream.open(fileLocation);
  if (inStream.fail())
  {
      std::cout << "Reading file error.";

  }

  int sampleCounter = 0;
  while(inStream>>passphase)
  {
  //        cout<<passphase;

      std::vector<std::string> sampleCodeAndCountry;
      boost::split(sampleCodeAndCountry, passphase, [](char c){return c == ',';});

      sample newSample;
      newSample.companyCode = stoi(sampleCodeAndCountry[0]);
      newSample.companyCountry = stoi(sampleCodeAndCountry[1]);

      sampleVector->push_back(newSample);
      sampleCounter++;
  }
  inStream.close();

  *sampleCount = sampleCounter;
}


template<typename Graph>
void
run_weighted_test(Graph*, int V, std::vector<weighted_edge> edge_init, int E, int baseCompany, int baseCountry)
{
  Graph g(V);
  typedef typename boost::graph_traits<Graph>::vertex_descriptor Vertex;
  typedef typename boost::graph_traits<Graph>::vertex_iterator vertex_iterator;
  typedef typename boost::graph_traits<Graph>::edge_descriptor Edge;


  std::vector<Vertex> vertices(V);
  {
    vertex_iterator v, v_end;
    int index = 0;
    for (boost::tie(v, v_end) = boost::vertices(g); v != v_end; ++v, ++index) {
      put(boost::vertex_index, g, *v, index);
      vertices[index] = *v;
    }
  }

  int edgeAddedCounter = 0;
  std::vector<Edge> edges(E);
  for (int e = 0; e < E; ++e) {

    if (((edge_init[e].source != baseCompany) && (edge_init[e].target != baseCompany)) // when, both the source and the target is NOT base company, and,
        && ((edge_init[e].sourceCountry == baseCountry) ||  (edge_init[e].sourceCountry == baseCountry))) // either the source or the targe is in the base counry
          continue; // droup the edge

    // otherwise: either the source and the target is the base company, or, both source and the target is out of the base country
    add_edge(vertices[edge_init[e].source], vertices[edge_init[e].target], {edge_init[e].weight}, g);
    edgeAddedCounter++;
  }

  std::cout <<"sample number" << baseCompany << "edge actually added:" << edgeAddedCounter << '\n';

  std::vector<double> centrality(V);
  brandes_betweenness_centrality(
    g,
    centrality_map(
      make_iterator_property_map(centrality.begin(), get(boost::vertex_index, g),
                                 double()))
    .vertex_index_map(get(boost::vertex_index, g)).weight_map(get(boost::edge_weight, g)));

    std::ofstream graphStream;
    graphStream.open(std::to_string(baseCompany)+"at"+std::to_string(baseCompany)+".txt");
    for (int v = 0; v < V; ++v) {
      graphStream << v << "," << centrality[v] << std::endl;
    }
    graphStream.close();
}


int main(int argc, char* argv[])
{
  std::string edgeListFile = "rel3Country.csv";
  std::string sampleListFile = "sample.csv";

  std::vector<sample> sampleList;
  int sampleCount = 0;


  typedef boost::adjacency_list<boost::listS, boost::listS, boost::undirectedS,
                         boost::property<boost::vertex_index_t, int>, EdgeProperties>
    Graph;

  std::vector<weighted_edge> edgeVector;
  int vCount, eCount;
  readSampleList(&sampleList, &sampleCount, sampleListFile); // Read a list of sample companies
  readedgelist(&edgeVector, &vCount, &eCount, edgeListFile); // read the edge list

  for (int i =0; i<sampleCount; i++)
  {
    std::cout << "Have Sample:" << sampleList[i].companyCode << " in Country number " <<sampleList[i].companyCountry << '\n';
  }


  for (int i =0; i<sampleCount; i++)
  {
      std::cout << "Processing Sample:" << sampleList[i].companyCode << " in Country number " <<sampleList[i].companyCountry << '\n';
      run_weighted_test((Graph*)0, vCount, edgeVector, eCount, sampleList[i].companyCode, sampleList[i].companyCountry);
  }

  return 0;
}
