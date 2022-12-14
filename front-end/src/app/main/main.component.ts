import { Component, OnInit } from '@angular/core';
import { Observable, take } from 'rxjs';
import { Document, Corpus } from '../models';
import { SearchService } from '../search.service';

@Component({
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss'],
})
export class MainComponent implements OnInit {
  constructor(private searchService: SearchService) {}

  ngOnInit(): void {}

  searchText: string = '';
  corpora$: Observable<Corpus[]> = this.searchService.getCorpora();
  corpus: string = 'cranfield';
  model: 'boolean' | 'vectorial' | 'lsi' = 'vectorial';
  results$!: Observable<Document[]>;
  loading = false;

  search() {
    this.results$ = this.searchService.search(
      this.searchText,
      this.model,
      this.corpus
    );
    this.loading = true;
    this.results$.pipe(take(1)).subscribe((results) => {
      this.loading = false;
    });
  }
}
