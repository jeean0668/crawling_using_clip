import torch
import crawler

if __name__ == "__main__":
    
    custom_crawler = crawler.GoogleImageCrawler()
    custom_crawler.search("dark cloud images")
    
    