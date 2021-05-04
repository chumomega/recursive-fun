package recfun

import scala.annotation.tailrec
import scala.collection.mutable

object RecFun extends RecFunInterface {

  def main(args: Array[String]): Unit = {
    println("Pascal's Triangle")
    for (row <- 0 to 10) {
      for (col <- 0 to row)
        print(s"${pascal(col, row)} ")
      println()
    }
  }

  /**
   * Exercise 1
   * get the nnumber in pascals triangle given a column and row number
   */
  def pascal(c: Int, r: Int): Int = ???

  /**
   * Exercise 2
   * this will take in a list of char and we need to say if its a balanced array of parentheses or not
   */
  def balance(chars: List[Char]): Boolean = {
    @tailrec
    def stackRec(paren: mutable.Stack[Char], chars: List[Char]): Boolean = {
      if (chars.isEmpty) true
      else {

        if (chars.head == ')' && paren.isEmpty) {
          false
        }
        else {
          if (chars.head == ')' && paren.top == '(') {
            paren.pop()
          }

          if (chars.head == '(') {
            paren.push(chars.head)
          }
          stackRec(paren, chars.tail)
        }
      }

    }
    stackRec(mutable.Stack[Char](), chars)
  }

  balance("hllo(world)xyz".toList)
  /**
   * Exercise 3
   * how many ways are there to make change given the denominations of coins
   * without dynamic programming, we calculate some problems repeatedly and this can be seen by drawing out the recursive tree
   */
  def countChange(money: Int, coins: List[Int]): Int = {
    def count(money: Int, coins: List[Int], coin_index_to_omit: Int): Int = {
      if (money == 0) 1
      else if (money < 0) 0
      else if (coin_index_to_omit <= 0 && money >= 1) 0
      else count(money, coins, coin_index_to_omit-1) +
        count(money - coins(coin_index_to_omit - 1), coins, coin_index_to_omit)
    }
    count(money,coins, coins.length)
  }
}
