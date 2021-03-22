import { Pipe, PipeTransform } from '@angular/core';
import { Evenement, Status } from '../evenements.service';

@Pipe({
  name: 'filterStatus'
})
export class FilterStatusPipe implements PipeTransform {

  transform(events: Evenement[], activeFilter: Status): unknown {
    return events.filter(event => event.status === activeFilter);
  }

}
