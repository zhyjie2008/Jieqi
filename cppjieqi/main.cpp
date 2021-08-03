// copyright 2021 miaosi@all rights reserved.
//#include <QCoreApplication>
#include <stdio.h>
#include <iostream>
#include <time.h>
#include "board/board.h"
#include "log/log.h"
#include "global/global.h"
#include "score/score.h"

extern void register_scoring_functions();

int main(void) {
    //QCoreApplication a(argc, argv);
    register_score_functions();
    printf("Hello Jieqi!\n");
    board::Board b;
    std::cout << std::get<3>(b.GetTuple()) << "\n";
    b.PrintPos(true);
    //b.Move(std::make_pair<int, int>(0, 0), std::make_pair<int, int>(1, 0));
    b.PrintPos(false);
    log::Log* l = Singleton<log::Log>::get();
    l -> SetConfig("F");
    size_t start = (size_t)clock();
    b.SetTurn(false);
    b.SetScoreFunction((std::string)"trivial_score_function");
    for(int i = 0; i < 10000000; ++i){
        b.GenMovesWithScore();
    }
    printf("%d\n", b.num_of_legal_moves);
    size_t end = (size_t)clock();
    printf("%d %lf\n", b.num_of_legal_moves, (double)(end - start)/CLOCKS_PER_SEC);
    b.PrintAllMoves();
    Singleton<log::Log>::deleteT();
    return 0;
}
