function [ number ] = generaterandom(range)
  %generateRandom Generates a random number.
  number = rand;
  number = number*range;
end

    