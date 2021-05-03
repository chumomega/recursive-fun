package recfun

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
  def balance(chars: List[Char]): Boolean = ???

  /**
   * Exercise 3
   * how many ways are there to make change given the denominations of coins
   */
  def countChange(money: Int, coins: List[Int]): Int = ???
}
