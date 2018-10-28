
#include "pch.h"
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

struct networkedge {
	string node1;
	string node2;
	int weight;
};

vector<networkedge> readfiles();

vector<networkedge> readfiles()
{
	vector<networkedge> df;


	ifstream inStream;
	string passphase;
	const string path = "C:\\Users\\Chilly Lin\\Documents\\coding\\RA-Combine\\DividedbyindustryC\\MANU";

	const string filename[3] = { "node1","node2","weight" };

	//First node
	inStream.open(path + filename[0] + ".csv");

	if (inStream.fail())
	{
		std::cout << "Reading file error.";
		return df;
	}

	vector<string> node1list;
	string node1name;

	while (inStream >> node1name)
	{

		node1list.push_back(node1name);

	}

	inStream.close();

	// Second node
	inStream.open(path + filename[1] + ".csv");

	if (inStream.fail())
	{
		std::cout << "Reading file error.";
		return df;
	}

	vector<string> node2list;
	string node2name;

	while (inStream >> node2name)
	{

		node2list.push_back(node2name);

	}
	inStream.close();

	// Weight
	inStream.open(path + filename[2] + ".csv");

	if (inStream.fail())
	{
		std::cout << "Reading file error.";
		return df;
	}

	vector<int> weightlist;
	int edgeweight;

	while (inStream >> edgeweight)
	{

		weightlist.push_back(edgeweight);

	}


	networkedge tempedge;

	while (!node1list.empty())
	{
		tempedge.node1 = node1list.back();
		tempedge.node2 = node2list.back();
		tempedge.weight = weightlist.back();
		

		node1list.pop_back();
		node2list.pop_back();
		weightlist.pop_back();

		df.push_back(tempedge);
	}

	return df;

}
